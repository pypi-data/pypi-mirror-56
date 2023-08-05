# jackdaw
gather gather gather

![jackdaw_small](https://user-images.githubusercontent.com/19204702/57587578-6159b280-7507-11e9-8762-c5e9022e37bc.png)


# What is this?
Jackdaw is here to collect all information in your domain, store it in a SQL database and show you nice graphs on how your domain objects interact with each-other an how a potential attacker may exploit these interactions.
It also comes with a handy feature to help you in a password-cracking project by storing/looking up/reporting hashes/passowrds/users.

# Example commands
### Enumeration
#### Full enumeration with integrated sspi
`jackdaw --sql sqlite:///test.db enum 'ldap://TEST\victim:Passw0rd!@10.10.10.2' 'smb+ntlm-password://TEST\victim:Passw0rd!@10.10.10.2'`
#### LDAP-only enumeration with username and password
The passowrd is `Passw0rd!`  
`jackdaw --sql sqlite:///test.db ldap 'ldap://TEST\victim:Passw0rd!@10.10.10.2'`

### Start interactive web interface to plog graph and access additional features
`jackdaw --sql sqlite:///<FULL PATH TO DB> nest`  
Open `http://127.0.0.1:5000/ui` for the API  
Open `http://127.0.0.1:5000/nest` for the graph interface 

# Features
## Data acquisition 
#### via LDAP
LDAP enumeration phase acquires data on AD info, User, Machine, OU, Group objects which will be reprezented as a node in the graph, and as a separate table in the DB. Additionally all afforementioned objects' Security Descriptior will be parsed and the ACLs for the DACL added to the DB. This, together with the memebership information will be represented as edges in the garph. Additionally custom SQL queries can be performed on any of the afforementioned data types when needed.  

#### via SMB
SMB enumeration phase acquires data on shares, localgroups, sessions, NTLM data via connecting to each machine in the domain (which is acquired via LDAP)  

#### via LSASS dumps (optional)  
The framework allows users to upload LSASS memory dumps to store credentials and extend the session information table. Both will be used as additional edges in the graph (shared password and session respectively). The framework also uses this information to create a password report on weak/shared/cracked credentials.  

#### via DCSYNC results (optional)
The framework allows users to upload impacket's DCSYNC files to store credentials. This be used as additional edges in the graph (shared password). The framework also uses this information to create a password report on weak/shared/cracked credentials.  

#### via manual upload (optional)
The framework allows manually extending the available DB in every aspect. Example: when user session information on a given computer is discovered (outside of the automatic enumeration) there is a possibility to manually upload these sessions, which will populate the DB and also the result graph

## Graph
The framework can generate a graph using the available information in the database and plot it via the web UI (nest). Furthermore the graph generation and path canculations can be invoked programmatically, either by using the web API (/ui endpoint) or the grph object's functions.  

## Anomlaies detection  
The framework can identify common AD misconfigurations without graph generation. Currently only via the web API.  

#### User
User anomalies detection involve detection of insecure UAC permissions and extensive user description values. This feature set is expected to grow in the future as new features will be implemented.

#### Machine
Machine anomalies detection involve detection of insecure UAC permissions, non-mandatory SMB singing, outdated OS version, out-of-domain machines. This feature set is expected to grow in the future as new features will be implemented.

## Password cracking
**The framework is not performing any cracking, only organizing the hashes and the cracking results**  
**currently main focus is on impacket and aiosmb's dcsync results !NT and LM hashes only!**  
Sample porcess is the following:  
1. Harvesting credentials as text file via impacket/aiosmb or as memory dumps of the LSASS process via whatever tool you see fit.
2. Upload the harvested credentials via the API
3. Poll uncracked hases via the API
4. Crack them (hashcat?)
5. Upload the results to the framework via the API
6. Generate a report on the cracked/uncracked users and password strength and password sharing
  
*note form author: This feature was implemented for both attackers and defenders. Personally I don't see much added value on either side, since at the point one obtained the NT hash of a user it's just as good as the password... Nonetheless, more and more companies are performing password strength excercises, and this feature would help them. As for attackers: it is just showing off at this point, but be my guest. Maybe scare management for extra points.*  


# Important
This project is in experimental phase! This means multiple things:
1. it may crash
2. the controls you are using might change in the future (most likely)
3. (worst part) The database design is not necessary suitable for future requests so it may change. There will be no effort to maintain backwards compatibility with experimental-phase DB structure!


# Technical part
## Database backend
Jackdaw uses SQLAlchemy ORM module, which gives you the option to use any SQL DB backend you like. The tests are mainly done on SQLite for ovbious reasons. There will be no backend-specific commands used in this project that would limit you.
