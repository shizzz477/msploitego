#!/usr/bin/env python
import re

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

webservices = ["http", "https", "possible_wls", "www", "ncacn_http", "ccproxy-http", "ssl/http","http-proxy"]
sambaservices = ["samba", "netbios-ssn", "smb", "microsoft-ds", "netbios-ns", "netbios-dgm", "netbios"]

def getserviceentity(s):
    entityname = "msploitego.MetasploitService"
    try:
        servicename = s.get("servicename").lower()
    except AttributeError:
        servicename = "NoName"
    try:
        serviceinfo = s.get("info").lower()
    except AttributeError:
        serviceinfo = None
    if s.get("state").lower() in ["filtered", "closed"]:
        return "msploitego.ClosedPort"
    else:
        if not servicename and not serviceinfo.strip():
            return "msploitego.MetasploitService"
        if any(x in servicename for x in webservices):
            if serviceinfo:
                if "iis" in s.get("info").lower():
                    return "msploitego.IISWebservice"
                elif "rpc over http" in s.get("info").lower():
                    return "msploitego.RPCoverhttp"
                elif "oracle xml db" in s.get("info").lower():
                    return "msploitego.OracleXMLDB"
                elif "apache" in s.get("info").lower():
                    if "apache tomcat" in s.get("info").lower():
                        return "msploitego.ApacheTomcat"
                    elif all(x in s.get("info").lower() for x in ["apache", "php"]):
                        return "msploitego.ApachePHP"
                    else:
                        return "msploitego.Apachehttpd"
                elif "httpfileserver" in s.get("info").lower():
                    return "msploitego.HTTPFileServer"
                elif "lighttpd" in s.get("info").lower():
                    return "msploitego.lighttpd"
                elif "nginx" in s.get("info").lower():
                    return "msploitego.nginx"
                elif "jetty" in s.get("info").lower():
                    return "msploitego.Jetty"
                elif "node.js" in s.get("info").lower():
                    return "msploitego.Nodejs"
                elif "httpapi" in s.get("info").lower():
                    return "msploitego.MicrosoftHTTPAPI"
                elif "WAF" in s.get("info"):
                    return "msploitego.WAF"
                elif "oracle http server" in s.get("info").lower():
                    return "msploitego.OracleHTTPServer"
                elif "oracle xml db" in s.get("info").lower():
                    return "msploitego.OracleXMLDB"
                elif "goahead" in s.get("info").lower():
                    return "msploitego.GoAheadWebServer"
                elif "webmin" in s.get("info").lower():
                    return "msploitego.Webmin"
                elif "rocket" in s.get("info").lower():
                    return "msploitego.RocketWebServer"
                elif "squid" in s.get("info").lower():
                    return "msploitego.SquidProxyServer"
                elif "vpn" in s.get("info").lower():
                    return "msploitego.CiscoVPN"
                elif "communigate" in s.get("info").lower():
                    return "msploitego.CommuniDatePro"
                else:
                    return "msploitego.WebService"
            else:
                return "msploitego.WebService"
        elif s.get("port") == "32768":
            return "msploitego.PotentialBackdoor"
        elif any(x in servicename for x in sambaservices):
            return "msploitego.SambaService"
        elif servicename == "ssh":
            return "msploitego.SSHService"
        elif servicename in ["dns", "mdns", "domain"]:
            return "msploitego.DNSService"
        elif any(x in servicename for x in ["rpc","portmap"]):
            return "msploitego.RPC"
        elif "epmap" in servicename:
            return "msploitego.epmap"
        elif "cifs" in servicename:
            return "msploitego.cifs"
        elif "ssdp" in servicename:
            return "msploitego.ssdp"
        elif "irc" in servicename:
            return "msploitego.irc"
        elif "pop" in servicename:
            return "msploitego.pop3"
        elif "oracle" in servicename:
            return "msploitego.Oracle"
        elif "ftp" in servicename:
            return "msploitego.ftp"
        elif "finger" in servicename:
            return "msploitego.finger"
        elif "imap" in servicename:
            return "msploitego.imap"
        elif "winrm" in servicename:
            return "msploitego.winrm"
        elif "nmap" in servicename:
            return "msploitego.Nmap"
        elif "ldap" in servicename:
            return "msploitego.LDAP"
        elif "compressnet" in servicename:
            return "msploitego.compressnet"
        elif "ansys" in servicename:
            return "msploitego.ansys"
        elif "boinc" in servicename:
            return "msploitego.boinc"
        elif "bakbone" in servicename:
            return "msploitego.bakbonenetvault"
        elif "cisco" in servicename:
            return "msploitego.CISCO"
        elif "ntp" in servicename:
            return "msploitego.ntp"
        elif "dhcp" in servicename:
            return "msploitego.DHCP"
        elif "dbase" in servicename:
            return "msploitego.dBase"
        elif "chargen" in servicename:
            return "msploitego.chargen"
        elif "directplaysrvr" in servicename:
            return "msploitego.directplaysrvr"
        elif "smtp" in servicename:
            return "msploitego.smtp"
        elif "ident" in servicename:
            return "msploitego.ident"
        elif any(x in servicename for x in ["snmp", "smux"]):
            return "msploitego.SNMP"
        elif "tcpwrapped" in servicename:
            return "msploitego.tcpwrapped"
        elif "mysql" in servicename:
            return "msploitego.mysql"
        elif any(x in servicename for x in ["mssql", "ms-sql", "dbm"]):
            return "msploitego.mssql"
        elif any(x in servicename for x in ["nat-pmp", "upnp", "natpmp"]):
            return "msploitego.natpmp"
        elif any(x in servicename for x in ["confluent", "kafka"]):
            return "msploitego.ApacheKafka"
        elif any(x in servicename for x in ["ndmp"]):
            return "msploitego.NAS"
        elif any(x in servicename for x in ["neod", "corba"]):
            return "msploitego.ObjectRequestBroker"
        elif "ajp" in servicename:
            return "msploitego.ajp"
        elif "llmnr" in servicename:
            return "msploitego.llmnr"
        elif any(x in servicename for x in ["keysrvr", "keyshadow"]):
            return "msploitego.KeyServer"
        elif servicename in ["kerberos", "kpasswd5", "kerberos-sec", "krb524"]:
            return "msploitego.kerberos"
        elif "msexchange-logcopier" in servicename:
            return "msploitego.MSExchangeLogCopier"
        elif any(x in servicename for x in ["nfs", "lockd", "amiganetfs","mountd","nlockmgr"]):
            return "msploitego.nfsacl"
        elif "x11" in servicename:
            return "msploitego.X11"
        elif re.search("\bsip\b|sip-proxy", servicename, re.I):
            return "msploitego.SIP"
        elif "fmtp" in servicename:
            return "msploitego.fmtp"
        elif "telnet" in servicename:
            return "msploitego.telnet"
        elif any(x in servicename for x in ["rdp", "xdmcp"]):
            return "msploitego.rdp"
        elif "ipp" in servicename:
            return "msploitego.ipp"
        elif "vnc" in servicename:
            return "msploitego.vnc"
        elif "wap-wsp" in servicename:
            return "msploitego.wapwsp"
        elif "blackjack" in servicename:
            return "msploitego.blackjack"
        elif any(x in servicename for x in ["backorifice", "bo2k"]):
            return "msploitego.backorifice"
        elif "rtsp" in servicename:
            return "msploitego.rtsp"
        elif "bacnet" in servicename:
            return "msploitego.Bacnet"
        elif "msdtc" in servicename:
            return "msploitego.msdtc"
        elif "wfremotertm" in servicename:
            return "msploitego.wfremotertm"
        elif "msdp" in servicename:
            return "msploitego.msdp"
        elif "ssl" in servicename:
            return "msploitego.ssl"
        elif all(x in servicename for x in ["afs", "fileserver"]):
            return "msploitego.AFS"
        elif "adobeserver" in servicename:
            return "msploitego.AdobeserverService"
        elif "ms-wbt-server" in servicename:
            return "msploitego.MicrosoftTerminalServices"
        elif servicename in ["rmiregistry", "java-rmi"]:
            return "msploitego.JavaRMI"
        elif re.match("^ams$", servicename, re.I):
            return "msploitego.AdvancedMultithreadedServer"
        elif re.search("landesk", servicename, re.I):
            return "msploitego.Landesk"
        elif re.search("xmpp", servicename, re.I):
            return "msploitego.xmpp"
        elif any(x in servicename for x in ["lansource","citrix"]):
            return "msploitego.Lansource"
    return entityname

def getosentity(osfamily,osname):
    osentityname = "msploitego.OperatingSystem"
    osdescription = "Operating System"
    if osname or osfamily:
        if osfamily:
            if osname:
                if "windows 2003" in osname.lower():
                    osentityname = "msploitego.Windows2003"
                elif "windows 2008" in osname.lower():
                    osentityname = "msploitego.Windows2008"
                elif "windows 2012" in osname.lower():
                    osentityname = "msploitego.Windows2012"
                elif "windows 2000" in osname.lower():
                    osentityname = "msploitego.Windows2000"
                elif "windows xp" in osname.lower():
                    osentityname = "msploitego.WindowsXP"
                elif "windows 7" in osname.lower():
                    osentityname = "msploitego.Windows7"
                elif "freebsd" in osname.lower():
                    osentityname = "msploitego.FreeBSD"
                elif "solaris" in osname.lower():
                    osentityname = "msploitego.Solaris"
                elif "linux" in osname.lower():
                    osentityname = "msploitego.LinuxOperatingSystem"
                elif "embedded" in osname.lower():
                    osentityname = "msploitego.EmbeddedOS"
                elif re.search("ios", osname.lower(), re.I):
                    osentityname = "msploitego.IOS"
                osdescription = osname
            else:
                if "windows" in osfamily.lower():
                    osentityname = "msploitego.WindowsOperatingSystem"
                elif "freebsd" in osfamily.lower():
                    osentityname = "msploitego.FreeBSD"
                elif "linux" in osfamily.lower():
                    osentityname = "msploitego.LinuxOperatingSystem"
                osdescription = osfamily
        elif osname:
            if "embedded" in osname.lower():
                osentityname = "msploitego.EmbeddedOS"
            elif "linux" in osname.lower():
                osentityname = "msploitego.LinuxOperatingSystem"
            elif re.search("ios",osname.lower(),re.I):
                osentityname = "msploitego.IOS"
            elif re.search("diskstation\smanager",osname.lower(),re.I):
                osentityname = "msploitego.DiskstationManager"
            osdescription = osname
    return [osentityname,osdescription]
