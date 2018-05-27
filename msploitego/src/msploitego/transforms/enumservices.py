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
    servicecount = int(mt.getVar("servicecount"))
    if servicecount > 0:
        for service in MetasploitXML(fn).gethost(ip).services:
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
                elif servicename in ["samba","netbios-ssn","smb","microsoft-ds"]:
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
                elif "winrm" in servicename:
                    entityname = "msploitego.winrm"
                elif "ldap" in servicename.lower():
                    entityname = "msploitego.LDAP"
                elif "ntp" in servicename:
                    entityname = "msploitego.ntp"
                elif "smtp" in servicename:
                    entityname = "msploitego.smtp"
                elif "snmp" in servicename:
                    entityname = "msploitego.SNMP"
                elif "tcpwrapped" in servicename:
                    entityname = "msploitego.tcpwrapped"
                elif "mysql" in servicename:
                    entityname = "msploitego.mysql"
                elif "mssql" in servicename:
                    entityname = "msploitego.mssql"
                elif "ajp" in servicename:
                    entityname = "msploitego.ajp"
                elif "llmnr" in servicename.lower():
                    entityname = "msploitego.llmnr"
                elif servicename.lower() in ["kerberos","kpasswd5","kerberos-sec"]:
                    entityname = "msploitego.kerberos"
                elif "msexchange-logcopier" in servicename.lower():
                    entityname = "msploitego.MSExchangeLogCopier"
                elif "nfs_acl" in servicename.lower():
                    entityname = "msploitego.nfsacl"
                elif "fmtp" in servicename.lower():
                    entityname = "msploitego.fmtp"
                elif "telnet" in servicename.lower():
                    entityname = "msploitego.telnet"
                elif "rdp" in servicename.lower():
                    entityname = "msploitego.rdp"
                elif "ipp" in servicename.lower():
                    entityname = "msploitego.ipp"
                elif "vnc" in servicename.lower():
                    entityname = "msploitego.vnc"
                elif "rtsp" in servicename.lower():
                    entityname = "msploitego.rtsp"
                elif "ms-wbt-server" in servicename.lower():
                    entityname = "msploitego.MicrosoftTerminalServices"
                elif servicename.lower() in ["rmiregistry", "java-rmi"]:
                    entityname = "msploitego.JavaRMI"
                #msploitego.JavaRMI
            hostservice = mt.addEntity(entityname, "{}/{}:{}".format(servicename,service.port,service.hostid))
            hostservice.setValue = "{}/{}:{}".format(servicename,service.port,service.hostid)
            hostservice.addAdditionalFields("ip","IP Address",False,ip)
            if servicename and servicename.lower() in ["http","www","https"]:
                hostservice.addAdditionalFields("niktofile", "Nikto File", False, '')
            hostservice.addAdditionalFields("fromfile", "Source File", False, fn)
            hostservice.addAdditionalFields("service.name", "Service Name", False, servicename)
            if service.containsTag("info"):
                hostservice.addAdditionalFields("banner", "Banner", False, service.info)
            else:
                hostservice.addAdditionalFields("banner", "Banner", False, "{}-No info".format(servicename))
            for etag in entitytags:
                if etag in service.getTags():
                    val = service.getVal(etag)
                    hostservice.addAdditionalFields(etag, etag, False, val)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['enumservices.py',
#  '10.11.1.115',
#  'ipv4-address=10.11.1.115#ipaddress.internal=false#notecount=3#address=10.11.1.115#purpose=server#mac=00:50:56:b8:e9:18#osfamily=Linux#servicecount=9#name=tophat.acme.com#state=alive#vulncount=1#fromfile=/root/data/report_pack/msploitdb_oscp-20180325.xml#osname=Linux']
#
# dotransform(args)
