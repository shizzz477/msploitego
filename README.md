**msploitego - The Pentesting suite for Maltego**
=================================================

THIS IS A BETA RELEASE, please be nice and report any issues

msploitego leverages the data gathered in a Metasploit database by enumerating and creating specific entities for services.  Services like samba, smtp, snmp, http have transforms to enumerate even further

Requirements
============
- Python 2.7
- Has only been tested on Kali Linux
- software installations
  - Metasploit
  - nmap
  - enum4linux
  - smtp-check
  - nikto
  

Installation
============
- checkout and update the transform path inside Maltego
- In Maltego import config from msploitego/src/msploitego/resources/maltego/msploitego.mtz

General Use
===========
- run a db_nmap scan in metatasploit, or import a previous scan
  - msf> db_nmap -vvvv -T5 -A -sS -ST -Pn <target>
  - msf> db_import /path/to/your/nmapfile.xml
  
- export the database to an xml file
  - msf> db_export -f xml /path/to/your/output.xml

- In Maltego drag a MetasploitDBXML entity onto the graph.
- Update the entity with the path to your metasploit database file.
- run the MetasploitDB transform to enumerate hosts.
- from there several transforms are available to enumerate services, vulnerabilities stored in the metasploit DB

Notes
=====
- Instead of running a **nikto** scan directly from Maltego, I've opted to include a field to for a Nikto XML file.  Nikto can take  long time to run so best to manage that directly from the os.

TODO's
======
- Connect directly to the postgres database
- Much, much, much more tranforms for actions generated entities.
