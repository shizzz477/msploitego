#!/bin/bash
HOSTS=$1
REPODIRECTORY=$PWD/repo
WORKSPACE=$2
if [ -z "$HOSTS" ] || [ -z "$WORKSPACE" ]
then
	echo "Usage: msploitstarter.sh <hostrange or CIDR> <metasploit workspace>"
	exit 1
fi

mkdir -p $REPODIRECTORY

echo "running initial nmap scan within Metasploit...."
msfconsole -qx "workspace ${WORKSPACE}; db_nmap -vvvvv -sS -sU -sV -T5 -A ${HOSTS}; exit -y;"

echo "getting service information from metasploit db.."
msfconsole -qx "workspace ${WORKSPACE}; services; exit -y;" > $REPODIRECTORY/services.txt

echo "getting hosts information from metasploit db"
msfconsole -qx "workspace ${WORKSPACE}; hosts; exit -y;" > $REPODIRECTORY/hosts.txt

echo "running auxiliary module msfcrawler on http services..."
for url in $(cat $REPODIRECTORY/services.txt | grep open | grep http | awk '{print $1":"$2}'); do 
	HOST=$(echo $url | cut -d":" -f1);
	PORT=$(echo $url | cut -d":" -f2);
	msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/crawler/msfcrawler; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; run; exit -y;";
done

echo "running http auxiliary modules..."
for url in $(cat $REPODIRECTORY/services.txt | grep open | grep http | grep -v 443| awk '{print $1":"$2}'); do 
	HOST=$(echo $url | cut -d":" -f1);
	PORT=$(echo $url | cut -d":" -f2);
	msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/scanner/http/dir_listing; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set PATH /; set SSL false; run; use auxiliary/scanner/http/host_header_injection; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set TARGETHOST example.com; set SSL false; run; use auxiliary/scanner/http/http_header; set RHOSTS ${HOST}; set TARGETURI /; set IGN_HEADER Vary,Date,Content-Length,Connection,Etag,Expires,Pragma,Accept-Ranges; set RPORT ${PORT}; set THREADS 24; set HTTP_METHOD HEAD; run; use auxiliary/scanner/http/robots_txt; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set PATH /; set SSL false; run; use auxiliary/scanner/http/wordpress_scanner; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set TARGETURI /; set SSL false; run; exit -y;";
done

echo "running apache auxiliary modules..."
for url in $(cat $REPODIRECTORY/services.txt | grep open | grep -i apache | awk '{print $1":"$2}'); do 
	HOST=$(echo $url | cut -d":" -f1);
	PORT=$(echo $url | cut -d":" -f2);
	msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/scanner/http/apache_optionsbleed; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set TARGETURI /; set BUGS true; set SSL false; run; exit -y;";
done

echo "running iis auxiliary modules..."
for url in $(cat $REPODIRECTORY/services.txt | grep open | grep -i iis | awk '{print $1":"$2}'); do 
	HOST=$(echo $url | cut -d":" -f1);
	PORT=$(echo $url | cut -d":" -f2);
	msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/scanner/http/ms09_020_webdav_unicode_bypass; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set PATH /; set SSL false; run; exit -y;";
done

echo "running nginx auxiliary modules..."
for url in $(cat $REPODIRECTORY/services.txt | grep open | grep -i nginx | awk '{print $1":"$2}'); do 
	HOST=$(echo $url | cut -d":" -f1);
	PORT=$(echo $url | cut -d":" -f2);
	msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/scanner/http/nginx_source_disclosure; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set PATH /; set SSL false; set TARGETURI /admin.php; set PATH_SAVE ${REPODIRECTORY}; run; exit -y;";
done

echo "running windows related auxiliary modules..."
for HOST in $(cat $REPODIRECTORY/hosts.txt | grep -i windows | awk '{print $1}'); do 
	msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/scanner/http/ntlm_info_enumeration; set RHOSTS ${HOST}; set THREADS 24; set RPORT 80; set TARGET_URIS_FILE /usr/share/metasploit-framework/data/wordlists/http_owa_common.txt; set SSL false; run; use auxiliary/scanner/http/webdav_scanner; set RHOSTS ${HOST}; set THREADS 24; set RPORT 80; set SSL false; set PATH /; run; use auxiliary/scanner/http/webdav_website_content; set RHOSTS ${HOST}; set THREADS 24; set RPORT 80; set SSL false; set PATH /; run; exit -y;";
done

echo "running *nix web related auxiliary modules..."
for url in $(cat $REPODIRECTORY/services.txt | grep http | grep open | egrep -vi -e'microsoft|ftp|ssl' | awk '{print $1":"$2}'); do 
	HOST=$(echo $url | cut -d":" -f1);
	PORT=$(echo $url | cut -d":" -f2);
	msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/scanner/http/webpagetest_traversal; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set TARGETURI /; set FILE /etc/passwd; set DEPTH 11; run; set FILE /etc/shadow; run; exit -y;";
done

echo "running tomcat related auxiliary modules..."
for url in $(cat $REPODIRECTORY/services.txt | grep open | grep -i tomcat | awk '{print $1":"$2}'); do 
	HOST=$(echo $url | cut -d":" -f1);
	PORT=$(echo $url | cut -d":" -f2);
	msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/scanner/http/tomcat_enum; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set TARGETURI /admin/j_security_check; set SSL false; set USER_FILE /usr/share/metasploit-framework/data/wordlists/tomcat_mgr_default_users.txt; set DB_ALL_USERS false; set BRUTEFORCE_SPEED 5; set DB_ALL_PASS false; set DB_ALL_CREDS false; set VERBOSE true; run; exit -y;";
done

echo "running snmp auxiliary modules..."
for url in $(cat $REPODIRECTORY/services.txt | grep open | grep -i snmp | awk '{print $1":"$2}'); do 
	HOST=$(echo $url | cut -d":" -f1);
	PORT=$(echo $url | cut -d":" -f2);
	msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/scanner/snmp/snmp_enum; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set COMMUNITY public; set TIMEOUT 1; set VERSION 1; set RETRIES 1; run; use auxiliary/scanner/snmp/snmp_enumshares; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set COMMUNITY public; set TIMEOUT 1; set VERSION 1; set RETRIES 1; run; use auxiliary/scanner/snmp/snmp_enumusers; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set COMMUNITY public; set TIMEOUT 1; set VERSION 1; set RETRIES 1; run; exit -y;";
done

echo "running dcerpc endpoint mapper auxiliary modules..." 
for url in $(cat $REPODIRECTORY/services.txt | grep open | grep -i dcerpc | grep 135 | awk '{print $1":"$2}'); do 
	HOST=$(echo $url | cut -d":" -f1);
	PORT=$(echo $url | cut -d":" -f2);
	msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/scanner/dcerpc/endpoint_mapper; set RHOSTS ${HOST}; set THREADS 24; set RPORT 135; run; use auxiliary/scanner/dcerpc/management; set RHOSTS ${HOST}; set THREADS 24; set RPORT 135; run; use auxiliary/scanner/dcerpc/tcp_dcerpc_auditor; set RHOSTS ${HOST}; set THREADS 24; set RPORT 135; run; exit -y;";
done

echo "running dcerpc auxiliary modules..."
for HOST in $(cat $REPODIRECTORY/services.txt | grep dcerpc | grep open | awk '{print $1}' | sort -u); do 
	msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/scanner/dcerpc/hidden; set RHOSTS ${HOST}; set THREADS 24; run; exit -y;";
done

echo "running auxiliary modules on samba services..."
for HOST in $(cat $REPODIRECTORY/services.txt | grep open | egrep -e '445' | awk '{print $1}'); do 
	msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/scanner/smb/psexec_loggedin_users; set RHOSTS ${HOST}; set THREADS 24; set RPORT 445; set WINPATH WINDOWS; set SMBDomain .; set SMBSHARE C$; run; set SMBSHARE ADMIN$;run; set SMBSHARE IPC$; run; use auxiliary/scanner/smb/smb_enum_gpp; set RHOSTS ${HOST}; set SMBDomain .; set SMBSHARE SYSVOL; set STORE true; set THREADS 24; set RPORT 445; run; use auxiliary/scanner/smb/smb_ms17_010; set RHOSTS ${HOST}; set THREADS 24; set RPORT 445; set CHECK_ARCH true; set CHECK_PIPE false; set CHECK_DOPU true; set NAMED_PIPES /usr/share/metasploit-framework/data/wordlists/named_pipes.txt; run ;exit -y;";
done

echo "running auxiliary modules on samba services..."
for HOST in $(cat $REPODIRECTORY/services.txt | grep open | egrep -e '139|445' | awk '{print $1}'| sort -u); do
	msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/scanner/smb/pipe_auditor; set RHOSTS ${HOST}; set THREADS 24; set SMBDomain .; set NAMED_PIPES /usr/share/metasploit-framework/data/wordlists/named_pipes.txt; run; use auxiliary/scanner/smb/pipe_dcerpc_auditor; set RHOSTS ${HOST}; set THREADS 24; set SMBDomain .; set SMBPIPE BROWSER; run; use auxiliary/scanner/smb/smb_enumshares; set RHOSTS ${HOST}; set THREADS 24; set SMBDomain .; set ShowFiles true; set SpiderShares true; set SpiderProfiles true; set MaxDepth 999; run; use auxiliary/scanner/smb/smb_enumusers; set RHOSTS ${HOST}; set THREADS 24; set SMBDomain .; run; use auxiliary/scanner/smb/smb_enumusers_domain; set RHOSTS ${HOST}; set THREADS 24; set SMBDomain .; run; exit -y;";
done

echo "running brute force file locator for http services...this takes a long time"
for url in $(cat $REPODIRECTORY/services.txt | grep open | grep http | grep -v 443| awk '{print $1":"$2}'); do 
	HOST=$(echo $url | cut -d":" -f1);
	PORT=$(echo $url | cut -d":" -f2);
  msfconsole -qx "workspace ${WORKSPACE}; use auxiliary/scanner/http/files_dir; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set DICTIONARY /usr/share/metasploit-framework/data/wmap/wmap_files.txt; set PATH /; set SSL false; run; use auxiliary/scanner/http/http_traversal; set RHOSTS ${HOST}; set THREADS 24; set RPORT ${PORT}; set PATH /; set METHOD GET; set DEPTH 5; set FILELIST /usr/share/metasploit-framework/data/wordlists/sensitive_files.txt; set PATTERN (?-mix:^HTTP\/d.d 200); run; exit -y;";
done