#!/usr/bin/env python
import re

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def getserviceentity(s):
    entityname = "msploitego.MetasploitService"
    try:
        servicename = s.get("servicename")
    except AttributeError:
        servicename = "NoName"
    try:
        serviceinfo = s.get("info")
    except AttributeError:
        serviceinfo = None
    if s.get("state").lower() in ["filtered", "closed"]:
        return "msploitego.ClosedPort"
    else:
        if not servicename and not serviceinfo.strip():
            return "msploitego.MetasploitService"
        if servicename in ["http", "https", "possible_wls", "www", "ncacn_http", "ccproxy-http", "ssl/http",
                           "http-proxy"]:
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
                else:
                    return "msploitego.WebService"
            else:
                return "msploitego.WebService"
        elif s.get("port") == "32768":
            return "msploitego.PotentialBackdoor"
        elif any(
                x in servicename for x in ["samba", "netbios-ssn", "smb", "microsoft-ds", "netbios-ns", "netbios-dgm"]):
            return "msploitego.SambaService"
        elif servicename == "ssh":
            return "msploitego.SSHService"
        elif servicename in ["dns", "mdns", "domain"]:
            return "msploitego.DNSService"
        elif "rpc" in servicename:
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
        elif "winrm" in servicename.lower():
            return "msploitego.winrm"
        elif "nmap" in servicename.lower():
            return "msploitego.Nmap"
        elif "ldap" in servicename.lower():
            return "msploitego.LDAP"
        elif "compressnet" in servicename.lower():
            return "msploitego.compressnet"
        elif "ansys" in servicename.lower():
            return "msploitego.ansys"
        elif "boinc" in servicename.lower():
            return "msploitego.boinc"
        elif "bakbone" in servicename.lower():
            return "msploitego.bakbonenetvault"
        elif "cisco" in servicename.lower():
            return "msploitego.CISCO"
        elif "ntp" in servicename:
            return "msploitego.ntp"
        elif "dhcp" in servicename:
            return "msploitego.DHCP"
        elif "dbase" in servicename.lower():
            return "msploitego.dBase"
        elif "chargen" in servicename.lower():
            return "msploitego.chargen"
        elif "directplaysrvr" in servicename:
            return "msploitego.directplaysrvr"
        elif "smtp" in servicename.lower():
            return "msploitego.smtp"
        elif "ident" in servicename.lower():
            return "msploitego.ident"
        elif any(x in servicename.lower() for x in ["snmp", "smux"]):
            return "msploitego.SNMP"
        elif "tcpwrapped" in servicename:
            return "msploitego.tcpwrapped"
        elif "mysql" in servicename:
            return "msploitego.mysql"
        elif any(x in servicename.lower() for x in ["mssql", "ms-sql", "dbm"]):
            return "msploitego.mssql"
        elif any(x in servicename for x in ["nat-pmp", "upnp", "natpmp"]):
            return "msploitego.natpmp"
        elif any(x in servicename.lower() for x in ["confluent", "kafka"]):
            return "msploitego.ApacheKafka"
        elif any(x in servicename for x in ["ndmp"]):
            return "msploitego.NAS"
        elif any(x in servicename.lower() for x in ["neod", "corba"]):
            return "msploitego.ObjectRequestBroker"
        elif "ajp" in servicename:
            return "msploitego.ajp"
        elif "llmnr" in servicename.lower():
            return "msploitego.llmnr"
        elif any(x in servicename.lower() for x in ["keysrvr", "keyshadow"]):
            return "msploitego.KeyServer"
        elif servicename.lower() in ["kerberos", "kpasswd5", "kerberos-sec", "krb524"]:
            return "msploitego.kerberos"
        elif "msexchange-logcopier" in servicename.lower():
            return "msploitego.MSExchangeLogCopier"
        elif any(x in servicename.lower() for x in ["nfs", "lockd", "amiganetfs"]):
            return "msploitego.nfsacl"
        elif "x11" in servicename.lower():
            return "msploitego.X11"
        elif "sip" == servicename.lower():
            return "msploitego.SIP"
        elif "fmtp" in servicename.lower():
            return "msploitego.fmtp"
        elif "telnet" in servicename.lower():
            return "msploitego.telnet"
        elif any(x in servicename.lower() for x in ["rdp", "xdmcp"]):
            return "msploitego.rdp"
        elif "ipp" in servicename.lower():
            return "msploitego.ipp"
        elif "vnc" in servicename.lower():
            return "msploitego.vnc"
        elif "wap-wsp" in servicename.lower():
            return "msploitego.wapwsp"
        elif "blackjack" in servicename.lower():
            return "msploitego.blackjack"
        elif any(x in servicename.lower() for x in ["backorifice", "bo2k"]):
            return "msploitego.backorifice"
        elif "rtsp" in servicename.lower():
            return "msploitego.rtsp"
        elif "bacnet" in servicename.lower():
            return "msploitego.Bacnet"
        elif "msdtc" in servicename.lower():
            return "msploitego.msdtc"
        elif "wfremotertm" in servicename.lower():
            return "msploitego.wfremotertm"
        elif "msdp" in servicename.lower():
            return "msploitego.msdp"
        elif "ssl" in servicename.lower():
            return "msploitego.ssl"
        elif all(x in servicename.lower() for x in ["afs", "fileserver"]):
            return "msploitego.AFS"
        elif "adobeserver" in servicename.lower():
            return "msploitego.AdobeserverService"
        elif "ms-wbt-server" in servicename.lower():
            return "msploitego.MicrosoftTerminalServices"
        elif servicename.lower() in ["rmiregistry", "java-rmi"]:
            return "msploitego.JavaRMI"
        elif re.match("^ams$", servicename, re.I):
            return "msploitego.AdvancedMultithreadedServer"
        elif re.search("landesk", servicename, re.I):
            return "msploitego.Landesk"
        elif any(x in servicename.lower() for x in ["lansource","citrix"]):
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
            osdescription = osname
    return [osentityname,osdescription]