# Msploitego, The Pentesting Suite for Maltego

Msploitego(Metasploitego) is designed to deliver granularity to Pentesting tasks while visualizing the results.  The objective is to have a single pallete for a number of tools which feed on eachother's results.  

This application is based on the Metasploit Framework connecting directly to Metasploit's Postgres database.  Also, you can use an exported xml file from Metasploit however expect performance issues.  The xml export file is missing a lot of data that the database has, so it's highly recommended to use the Postgres connection.

* Currently provides over 150 entities
* 55+ transforms
* more & more coming

Transform | Input Entity | Data Source | Description
------------ | ---------- | ----------- | ----------
Postgres msf Hosts | Postgresql DB | Postgres | Enumerates hosts in the database
Postgres Services | IPV4 Address | Postgres | Services in database for host 
Enum Web Pages | IPV4 Address | Postgres | forms and pages in the database
Enum Vulns | IPV4 Address | Postgres | vulnerabilities in the database
Enum Credentials | Postgresql DB | Postgres | Retrieve credentials gathered in the msf db
Comprimised Host Sessions | Postgresql DB | Postgres |Detailed session information from post-exploitation
Session details | Meterpreter Session | Postgres | Load details of actions on comprimised host session
Postgres Loot | IPv4 Address | Postgres | retrieves any loot stored in the database
MetasploitDB | MetasploitDBXMLFile | XML file | Enumerates hosts in the export file
Enum Metasploit Services | IPV4 Address | XML file | Enumerates services in the export file
Enum Metasploit Services | IPV4 Address | XML file | Enumerates services in the export file
Enum Forms and Webpages | IPV4 Address | XML file | forms and pages in the export file
Enum Vulnerabilities | IPV4 Address | XML file | vulnerabilities in the export file
Apache Vuln Scan | Apache http service | | Run NSE vuln scripts against target
CSRF Vuln Scan | Web Service |  | Scan site for potential CSRF Vulnerabilities
HTTP Enum Directories | Web Service | nmap | Enumerate directories on webserver
HTTP Secure Headers | Web Service | nmap | HTTP response headers related to security given in OWASP Secure Headers
PHP XSS Vuln Scan | Web Service | nmap | checks site for XSS vulnerabilities
HTTP vuln scan\[full\] | Web Service | nmap | runs all NSE vuln scripts against the host/port
Web Site Comments | Website | nmap | scans website for source code comments
Robots.txt | Website | nmap | Look for Robots.txt file and reads it
Nikto Parser | Web Service | nikto | takes the 'Nikto file' property and parses the file into entities
SMB Vuln Scan | Samba Service | nmap | Scan for SMB Vulns
Samba Enum Services | Samba Service | nmap | enumerate samba services
Samba Enum Shares | Samba Service | nmap | enumerate samba shares
Samba Enum Users | Samba Service | nmap | enumerate samba users
Samba Master Browsers | Samba Service | nmap | enumerate samba browsers
Samba Share Listing | Samba Share | python | enumerate samba browsers
Samba File Retrieval | Samba File | python | fetch a file on a samba server
SMB Scan | Samba Server | python | enumerate Samba Server **broken**
SMB Scan | samba Service | python | scan to get details for further enumeration **broken**
SMTP Scan | smtp Service | nmap | Scan smtp service
IMAP Scan | imap Service | nmap | Scan for capabilities and ntlm info
SSH Scan | ssh Service | nmap | Scan for ssh service
rdp Vuln Scan | rdp Service | nmap | Scan for rdp service
FTP Vuln Scan | ftp service | nmap | scans ftp service for vulnerabilities
Pop Scan | ftp service | nmap | scans pop service
DNS NS Id | DNS Service | nmap | Retrieves information from a DNS nameserver by requesting its nameserver ID
RPC Enum | RPC service | nmap | attempt to Enumerate rpc services
Exploit Query | Vulnerability | Metasploit Framework | query Metasploit for relevant exploits
Get Web File | Web URL | wget | attempts to retrieve a file ina web directory
To False Positive | Metasploit Module | conversion | mark a suggested vuln attack as false positive
To Checked | Metasploit Module | conversion | mark a suggested vuln attack as investigated
To Hacked | Metasploit Module | conversion | mark a suggested vuln attack as hacked
To Vulnerable | Metasploit Module | conversion | mark a suggested vuln attack confirming vulnerability
To URL\[from Nikto Detail\] | Nikto Detail | conversion | creates a URL entity
To Web File\[from Nikto Detail\] | Nikto Detail | conversion | creates a Web File entity
To URL\[from Web Dir\] | Web Directory | conversion | creates a URL entity
To Website\[from Web Service\] | Web Service | conversion | creates a Web Service entity

## Known Issues
- some Metasploit enitities like loot files sometimes contain a bad character which the MaltegoTransform class cannot process. This causes an exception and nothing returned. I've beaten my head against the wall trying to 'cleanse'/decode the data but to no avail.
