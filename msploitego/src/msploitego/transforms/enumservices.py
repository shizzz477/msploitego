import re
from pprint import pprint

from common.msploitdb import MetasploitXML
from common.MaltegoTransform import *
import sys

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    entitytags = ["hostid","info", "name", "port", "proto", "state"]
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    fn = mt.getVar("fromfile")
    ip = mt.getVar("address")
    mac = mt.getVar("mac")
    osname = mt.getVar("osname")
    osfamily = mt.getVar("osfamily")
    machinename = mt.getVar("name")
    servicecount = int(mt.getVar("servicecount"))
    mdb = MetasploitXML(fn)
    if servicecount > 0:
        host =  mdb.gethost(ip)
        # for form in host.webforms:
        #     formentity = mt.addEntity("msploitego.SiteURL", "http://{}:{}{}".format(ip,form.port,form.path))
        #     formentity.setValue("http://{}:{}{}".format(ip,form.port,form.path))
        #     formentity.addAdditionalFields("ip", "IP Address", True, ip)
        #     for k,v in form:
        #         if v and v.strip():
        #             formentity.addAdditionalFields(k, k.capitalize(), True, v)
        # for page in host.webpages:
        #     pageentity = mt.addEntity("msploitego.SiteURL", "http://{}:{}{}".format(ip, page.port, page.path))
        #     pageentity.setValue("http://{}:{}{}".format(ip, page.port, page.path))
        #     pageentity.addAdditionalFields("ip", "IP Address", True, ip)
        #     for k, v in page:
        #         if v and v.strip():
        #             pageentity.addAdditionalFields(k, k.capitalize(), True, v)

        for service in host.services:
            entityname = "msploitego.MetasploitService"
            try:
                servicename = service.name
            except AttributeError:
                servicename = "NoName"
            try:
                serviceinfo = service.info
            except AttributeError:
                serviceinfo = None
            if service.state.lower() in ["filtered", "closed"]:
                entityname = "msploitego.ClosedPort"
            else:
                if servicename in ["http","https","possible_wls","www","ncacn_http","ccproxy-http","ssl/http","http-proxy"]:
                    if serviceinfo:
                        if "iis" in service.info.lower():
                            entityname = "msploitego.IISWebservice"
                        elif "rpc over http" in service.info.lower():
                            entityname = "msploitego.RPCoverhttp"
                        elif "oracle xml db" in service.info.lower():
                            entityname = "msploitego.OracleXMLDB"
                        elif "apache" in service.info.lower():
                            if "apache tomcat" in service.info.lower():
                                entityname = "msploitego.ApacheTomcat"
                            elif all(x in service.info.lower() for x in ["apache", "php"]):
                                entityname = "msploitego.ApachePHP"
                            else:
                                entityname = "msploitego.Apachehttpd"
                        elif "httpfileserver" in service.info.lower():
                            entityname = "msploitego.HTTPFileServer"
                        elif "lighttpd" in service.info.lower():
                            entityname = "msploitego.lighttpd"
                        elif "nginx" in service.info.lower():
                            entityname = "msploitego.nginx"
                        elif "jetty" in service.info.lower():
                            entityname = "msploitego.Jetty"
                        elif "node.js" in service.info.lower():
                            entityname = "msploitego.Nodejs"
                        elif "httpapi" in service.info.lower():
                            entityname = "msploitego.MicrosoftHTTPAPI"
                        elif "WAF" in service.info:
                            entityname = "msploitego.WAF"
                        elif "oracle http server" in service.info.lower():
                            entityname = "msploitego.OracleHTTPServer"
                        elif "oracle xml db" in service.info.lower():
                            entityname = "msploitego.OracleXMLDB"
                        elif "goahead" in service.info.lower():
                            entityname = "msploitego.GoAheadWebServer"
                        #
                        else:
                            entityname = "msploitego.WebService"
                    else:
                        entityname = "msploitego.WebService"
                elif service.port == "32768":
                    entityname = "msploitego.PotentialBackdoor"
                elif any(x in servicename for x in  ["samba","netbios-ssn","smb","microsoft-ds","netbios-ns","netbios-dgm"]):
                    entityname = "msploitego.SambaService"
                elif servicename == "ssh":
                    entityname = "msploitego.SSHService"
                elif servicename in ["dns","mdns","domain"]:
                    entityname = "msploitego.DNSService"
                elif "rpc" in servicename:
                    entityname = "msploitego.RPC"
                elif "epmap" in servicename:
                    entityname = "msploitego.epmap"
                elif "cifs" in servicename:
                    entityname = "msploitego.cifs"
                elif "ssdp" in servicename:
                    entityname = "msploitego.ssdp"
                elif "irc" in servicename:
                    entityname = "msploitego.irc"
                elif "pop" in servicename:
                    entityname = "msploitego.pop3"
                elif "oracle" in servicename:
                    entityname = "msploitego.Oracle"
                elif "ftp" in servicename:
                    entityname = "msploitego.ftp"
                elif "finger" in servicename:
                    entityname = "msploitego.finger"
                elif "imap" in servicename:
                    entityname = "msploitego.imap"
                elif "winrm" in servicename.lower():
                    entityname = "msploitego.winrm"
                elif "nmap" in servicename.lower():
                    entityname = "msploitego.Nmap"
                elif "ldap" in servicename.lower():
                    entityname = "msploitego.LDAP"
                elif "compressnet" in servicename.lower():
                    entityname = "msploitego.compressnet"
                elif "ansys" in servicename.lower():
                    entityname = "msploitego.ansys"
                elif "boinc" in servicename.lower():
                    entityname = "msploitego.boinc"
                elif "bakbone" in servicename.lower():
                    entityname = "msploitego.bakbonenetvault"
                elif "cisco" in servicename.lower():
                    entityname = "msploitego.CISCO"
                elif "ntp" in servicename:
                    entityname = "msploitego.ntp"
                elif "dhcp" in servicename:
                    entityname = "msploitego.DHCP"
                elif "dbase" in servicename.lower():
                    entityname = "msploitego.dBase"
                elif "chargen" in servicename.lower():
                    entityname = "msploitego.chargen"
                elif "directplaysrvr" in servicename:
                    entityname = "msploitego.directplaysrvr"
                elif "smtp" in servicename.lower():
                    entityname = "msploitego.smtp"
                elif "ident" in servicename.lower():
                    entityname = "msploitego.ident"
                elif any(x in servicename.lower()for x in ["snmp", "smux"]):
                    entityname = "msploitego.SNMP"
                elif "tcpwrapped" in servicename:
                    entityname = "msploitego.tcpwrapped"
                elif "mysql" in servicename:
                    entityname = "msploitego.mysql"
                elif any(x in servicename.lower() for x in ["mssql","ms-sql","dbm"]):
                    entityname = "msploitego.mssql"
                elif any(x in servicename for x in ["nat-pmp","upnp", "natpmp"]):
                    entityname = "msploitego.natpmp"
                elif any(x in servicename.lower() for x in ["confluent", "kafka"]):
                    entityname = "msploitego.ApacheKafka"
                elif any(x in servicename for x in ["ndmp"]):
                    entityname = "msploitego.NAS"
                elif any(x in servicename.lower() for x in ["neod", "corba"]):
                    entityname = "msploitego.ObjectRequestBroker"
                elif "ajp" in servicename:
                    entityname = "msploitego.ajp"
                elif "llmnr" in servicename.lower():
                    entityname = "msploitego.llmnr"
                elif any(x in servicename.lower() for x in ["keysrvr", "keyshadow"]):
                    entityname = "msploitego.KeyServer"
                elif servicename.lower() in ["kerberos","kpasswd5","kerberos-sec","krb524"]:
                    entityname = "msploitego.kerberos"
                elif "msexchange-logcopier" in servicename.lower():
                    entityname = "msploitego.MSExchangeLogCopier"
                elif any(x in servicename.lower() for x in ["nfs", "lockd","amiganetfs"]):
                    entityname = "msploitego.nfsacl"
                elif "x11" in servicename.lower():
                    entityname = "msploitego.X11"
                elif "sip" == servicename.lower():
                    entityname = "msploitego.SIP"
                elif "fmtp" in servicename.lower():
                    entityname = "msploitego.fmtp"
                elif "telnet" in servicename.lower():
                    entityname = "msploitego.telnet"
                elif any(x in servicename.lower() for x in ["rdp","xdmcp"]):
                    entityname = "msploitego.rdp"
                elif "ipp" in servicename.lower():
                    entityname = "msploitego.ipp"
                elif "vnc" in servicename.lower():
                    entityname = "msploitego.vnc"
                elif "wap-wsp" in servicename.lower():
                    entityname = "msploitego.wapwsp"
                elif "blackjack" in servicename.lower():
                    entityname = "msploitego.blackjack"
                elif any(x in servicename.lower() for x in ["backorifice","bo2k"]):
                    entityname = "msploitego.backorifice"
                elif "rtsp" in servicename.lower():
                    entityname = "msploitego.rtsp"
                elif "bacnet" in servicename.lower():
                    entityname = "msploitego.Bacnet"
                elif "msdtc" in servicename.lower():
                    entityname = "msploitego.msdtc"
                elif "wfremotertm" in servicename.lower():
                    entityname = "msploitego.wfremotertm"
                elif "msdp" in servicename.lower():
                    entityname = "msploitego.msdp"
                elif "ssl" in servicename.lower():
                    entityname = "msploitego.ssl"
                elif all(x in servicename.lower() for x in ["afs","fileserver"]):
                    entityname = "msploitego.AFS"
                elif "adobeserver" in servicename.lower():
                    entityname = "msploitego.AdobeserverService"
                elif "ms-wbt-server" in servicename.lower():
                    entityname = "msploitego.MicrosoftTerminalServices"
                elif servicename.lower() in ["rmiregistry", "java-rmi"]:
                    entityname = "msploitego.JavaRMI"
                #msploitego.AdobeserverService
            hostservice = mt.addEntity(entityname, "{}/{}:{}".format(servicename,service.port,service.hostid))
            hostservice.setValue = "{}/{}:{}".format(servicename,service.port,service.hostid)
            hostservice.addAdditionalFields("ip","IP Address",True,ip)
            if servicename and servicename.lower() in ["http","https","possible_wls","www","ncacn_http","ccproxy-http","ssl/http","http-proxy"]:
                hostservice.addAdditionalFields("niktofile", "Nikto File", True, '')
            hostservice.addAdditionalFields("fromfile", "Source File", True, fn)
            hostservice.addAdditionalFields("service.name", "Service Name", True, servicename)
            if service.containsTag("info"):
                hostservice.addAdditionalFields("banner", "Banner", True, service.info)
                if servicename in ["samba", "netbios-ssn", "smb", "microsoft-ds"]:
                    if "workgroup" in service.info.lower():
                        groupname = service.info.lower().split("workgroup:",1)[-1].lstrip()
                        workgroup = mt.addEntity("maltego.Domain", groupname)
                        workgroup.setValue(groupname)
                        workgroup.addAdditionalFields("ip", "IP Address", True, ip)
            else:
                hostservice.addAdditionalFields("banner", "Banner", True, "{}-No info".format(servicename))
            for etag in entitytags:
                if etag in service.getTags():
                    val = service.getVal(etag)
                    hostservice.addAdditionalFields(etag, etag, True, val)
            if mac:
                macentity = mt.addEntity("maltego.MacAddress", mac)
                macentity.setValue(mac)
                macentity.addAdditionalFields("ip", "IP Address", True, ip)
            if machinename and re.match("^[a-zA-z]+",machinename):
                hostentity = mt.addEntity("msploitego.Hostname", machinename)
                hostentity.setValue(machinename)
                hostentity.addAdditionalFields("ip", "IP Address", True, ip)
            """ OS determination """
            osentityname = "msploitego.OperatingSystem"
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

                osentity = mt.addEntity(osentityname, osdescription)
                osentity.setValue(osdescription)
                osentity.addAdditionalFields("ip", "IP Address", True, ip)
                    # elif "linux" in osfamily.lower():
                    #     osfament = mt.addEntity("msploitego.LinuxOperatingSystem", osfamily)
                    #     osfament.setValue(osfamily)
                    #     osfament.addAdditionalFields("ip", "IP Address", True, ip)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['enumservices.py',
#  '10.11.1.50',
#  'ipv4-address=10.11.1.50#ipaddress.internal=false#notecount=6#address=10.11.1.50#purpose=server#mac=00:50:56:b8:f0:4a#osfamily=Windows#servicecount=10#name=BETHANY2#state=alive#vulncount=0#fromfile=/root/data/report_pack/msploitdb20180601.xml#osname=Windows 2012 R2']
# dotransform(args)
