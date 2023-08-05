from . import Basemodel, lf
import datetime
import hashlib
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Index

from pypykatz.pypykatz import pypykatz
from pypykatz.utils.crypto.winhash import LM, NT

# It may be tempting to use SIDs to link credentials with users in the domain
# However some credentials format don't give SIDs (impacket) others have SIDs 
# that only identify the primary user, but not the owner of the actual credential
# Summary: we need to use the ad_id and the username<->samaccountname
#

class Credential(Basemodel):
	__tablename__ = 'credentials'
	__table_args__ = (Index('Credential_uc', "ad_id", "domain", "username","nt_hash", "lm_hash", "history_no", unique = True), )

	id = Column(Integer, primary_key=True)
	ad_id = Column(Integer)
	domain = Column(String, index=True, nullable= False)
	username = Column(String, index=True, nullable= False)
	nt_hash = Column(String, index=True, nullable= False)
	lm_hash = Column(String, index=True, nullable= False)
	history_no = Column(Integer, index=True, nullable= False)
	cred_type = Column(String, index=True, nullable= False)
	
	def __init__(self, domain = None, username = None, nt_hash = None, lm_hash = None, history_no = None, ad_id = -1):
		self.domain = domain
		self.username = username
		self.nt_hash = nt_hash
		self.lm_hash = lm_hash
		self.history_no = history_no
		self.ad_id = ad_id

	@staticmethod
	def from_impacket_line(line, ad_id = -1):
		cred = Credential()
		userdomainhist, flags, lm_hash, nt_hash, *t = line.split(':')
		#parsing history
		m = userdomainhist.find('_history')
		history_no = 0
		if m != -1:
			history_no = int(userdomainhist.split('_history')[1]) + 1
			userdomainhist = userdomainhist.split('_history')[0]
		m = userdomainhist.find('\\')
		domain = '<LOCAL>'
		username = userdomainhist
		if m != -1:
			domain = userdomainhist.split('\\')[0]
			username = userdomainhist.split('\\')[1]
		cred.ad_id = ad_id
		cred.nt_hash = nt_hash
		cred.lm_hash = lm_hash
		cred.history_no = history_no
		cred.username = username
		cred.domain = domain
		cred.cred_type = 'dcsync'
		return cred

	@staticmethod
	def from_impacket_stream(stream, ad_id = -1):
		for line in stream:
			yield Credential.from_impacket_line(line.decode(), ad_id = ad_id)

	@staticmethod
	def from_impacket_file(filename, ad_id = -1):
		"""
		Remember that this doesnt populate the foreign keys!!! You'll have to do it separately!
		important: historyno will start at 0. This means all history numbers in the file will be incremented by one
		"""
		with open(filename, 'r') as f:
			for line in f:
				yield Credential.from_impacket_line(line, ad_id = ad_id)

	@staticmethod
	def from_lsass_stream(stream, ad_id = -1):
		from pypykatz.pypykatz import pypykatz
		mimi = pypykatz.parse_minidump_buffer(stream)
		return Credential.lsass_generator(mimi, ad_id = ad_id)

	@staticmethod
	def from_lsass_dump(filename, ad_id = -1):
		
		mimi = pypykatz.parse_minidump_file(filename)
		return Credential.lsass_generator(mimi, ad_id = ad_id)

	@staticmethod
	def lsass_generator(mimi, ad_id):

		for luid in mimi.logon_sessions:
			sid = mimi.logon_sessions[luid].sid

			for cred in mimi.logon_sessions[luid].msv_creds:
				cr = Credential()
				cr.ad_id = ad_id
				cr.nt_hash = cred.NThash.hex() if cred.NThash is not None else '31d6cfe0d16ae931b73c59d7e0c089c0'
				cr.lm_hash = cred.LMHash if cred.LMHash is not None else 'aad3b435b51404eeaad3b435b51404ee'
				cr.history_no = 0
				cr.username = cred.username if cred.username is not None else 'NA'
				cr.domain = cred.domainname if cred.domainname is not None else '<LOCAL>'
				cr.cred_type = 'msv'
				yield cr, None, sid

			for cred in mimi.logon_sessions[luid].wdigest_creds:
				if cred.password is not None:
					cr = Credential()
					cr.ad_id = ad_id
					cr.nt_hash = NT(cred.password).hex()
					cr.lm_hash = None
					cr.history_no = 0
					cr.username = cred.username if cred.username is not None else 'NA'
					cr.domain = cred.domainname if cred.domainname is not None else '<LOCAL>'
					cr.cred_type = 'wdigest'
					yield cr, cred.password, sid

			for cred in mimi.logon_sessions[luid].ssp_creds:
				if cred.password is not None:
					cr = Credential()
					cr.ad_id = ad_id
					cr.nt_hash = NT(cred.password).hex()
					cr.lm_hash = None
					cr.history_no = 0
					cr.username = cred.username if cred.username is not None else 'NA'
					cr.domain = cred.domainname if cred.domainname is not None else '<LOCAL>'
					cr.cred_type = 'ssp'
					yield cr, cred.password, sid

			for cred in mimi.logon_sessions[luid].livessp_creds:
				if cred.password is not None:
					cr = Credential()
					cr.ad_id = ad_id
					cr.nt_hash = NT(cred.password).hex()
					cr.lm_hash = None
					cr.history_no = 0
					cr.username = cred.username if cred.username is not None else 'NA'
					cr.domain = cred.domainname if cred.domainname is not None else '<LOCAL>'
					cr.cred_type = 'live_ssp'
					yield cr, cred.password, sid

			#for cred in mimi.logon_sessions[luid]['dpapi_creds']:
			# dpapi credentials are not used in this database (for now)

			for cred in mimi.logon_sessions[luid].kerberos_creds:
				if cred.password is not None:
					cr = Credential()
					cr.ad_id = ad_id
					cr.nt_hash = NT(cred.password).hex()
					cr.lm_hash = None
					cr.history_no = 0
					cr.username = cred.username if cred.username is not None else 'NA'
					cr.domain = cred.domainname if cred.domainname is not None else '<LOCAL>'
					cr.cred_type = 'kerberos'
					yield cr, cred.password, sid

			for cred in mimi.logon_sessions[luid].credman_creds:
				if cred.password is not None:
					cr = Credential()
					cr.ad_id = ad_id
					cr.nt_hash = NT(cred.password).hex()
					cr.lm_hash = None
					cr.history_no = 0
					cr.username = cred.username if cred.username is not None else 'NA'
					cr.domain = cred.domainname if cred.domainname is not None else '<LOCAL>'
					cr.cred_type = 'credman'
					yield cr, cred.password, sid

			for cred in mimi.logon_sessions[luid].tspkg_creds:
				if cred.password is not None:
					cr = Credential()
					cr.ad_id = ad_id
					cr.nt_hash = NT(cred.password).hex()
					cr.lm_hash = None
					cr.history_no = 0
					cr.username = cred.username if cred.username is not None else 'NA'
					cr.domain = cred.domainname if cred.domainname is not None else '<LOCAL>'
					cr.cred_type = 'tpskg'
					yield cr, cred.password, sid

				
	@staticmethod
	def from_aiosmb_stream(stream, ad_id = -1):
		for line in stream:
			if line is None or len(line) == 0:
				continue
			yield Credential.from_aiosmb_line(line.decode(), ad_id = ad_id)

	@staticmethod
	def from_aiosmb_file(filename, ad_id = -1):
		"""
		Remember that this doesnt populate the foreign keys!!! You'll have to do it separately!
		important: historyno will start at 0. This means all history numbers in the file will be incremented by one
		"""
		with open(filename, 'r') as f:
			for line in f:
				if line is None or len(line) == 0:
					continue
				yield Credential.from_aiosmb_line(line, ad_id = ad_id)


	@staticmethod
	def from_aiosmb_line(line, ad_id = -1):
		cred = Credential()
		line = line.strip()
		data = line.split(':')
		pw = None
		if data[0] == 'ntlm':
			cred.ad_id = ad_id
			cred.domain = data[1]
			cred.username = data[2]
			cred.nt_hash = data[5]
			cred.lm_hash = data[4]
			cred.history_no = 0
			cred.cred_type = 'aiosmb-dcsync-ntlm'

		elif data[0] == 'ntlm_history':
			cred.ad_id = ad_id
			cred.domain = data[1]
			cred.username = data[2]
			cred.nt_hash = data[5]
			cred.lm_hash = data[4]
			cred.history_no = int(data[6].replace('history_',''))
			cred.cred_type = 'aiosmb-dcsync-ntlm-history'

		elif data[0] == 'cleartext':
			cred.ad_id = ad_id
			_, cred.domain, cred.username, pw = line.split(':', 4) #reparsing needed, pw might contain colon
			
			cred.nt_hash = NT(pw).hex()
			cred.lm_hash = None
			cred.history_no = 0
			cred.cred_type = 'aiosmb-dcsync-cleartext'

		return cred, pw