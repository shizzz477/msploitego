**msploitego - The Pentesting suite for Maltego**
=================================================

![maltegosnapshot01](https://user-images.githubusercontent.com/9602322/40849078-f941f302-658e-11e8-83b1-62aea49c5b65.png)

![maltegosnapshot02a](https://user-images.githubusercontent.com/9602322/40849101-0abae328-658f-11e8-976a-25a9c70498e6.png)

![maltegosnapshot03a](https://user-images.githubusercontent.com/9602322/40849110-109aa79c-658f-11e8-92fc-75631c49c2a6.png)

THIS IS A BETA RELEASE, please be nice and report any issues

msploitego leverages the data gathered in a Metasploit database by enumerating and creating specific entities for services.  Services like samba, smtp, snmp, http have transforms to enumerate even further.  Entities can either be loaded from a Metasploit XML file or taken directly from the Postgres msf database

Requirements
============
- Python 2.7
- Has only been tested on Kali Linux
- software installations
  - Metasploit Framework
  - nmap
  - enum4linux
  - snmp-check
  - nikto
  - exploitdb

Installation
============
- checkout and update the transform path inside Maltego
- In Maltego import config from msploitego/src/msploitego/resources/maltego/msploitego.mtz

General Use
===========
Using exported Metasploit xml file
----------------------------------
- run a db_nmap scan in metatasploit, or import a previous scan
  - msf> db_nmap -vvvv -T5 -A -sS -ST -Pn <target>
  - msf> db_import /path/to/your/nmapfile.xml
  
  - export the database to an xml file
  - msf> db_export -f xml /path/to/your/output.xml

  - In Maltego drag a MetasploitDBXML entity onto the graph.
  - Update the entity with the path to your metasploit database file.
  - run the MetasploitDB transform to enumerate hosts.
  - from there several transforms are available to enumerate services, vulnerabilities stored in the metasploit DB

Using Postgres
--------------
- drag and drop a Postgresql DB entity onto the canvas, enter DB details.
- run the Postgresql transforms directly against a running DB

Notes
=====
- Instead of running a **nikto** scan directly from Maltego, I've opted to include a field to for a Nikto XML file.  Nikto can take  long time to run so best to manage that directly from the os.

TODO's
======
- Connect directly to the postgres database - **in progress**
- Much, much, much more tranforms for actions on generated entities.


