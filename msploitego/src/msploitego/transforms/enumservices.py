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
    servicecount = int(mt.getVar("servicecount"))
    # servicename = None
    if servicecount > 0:
        for service in MetasploitXML(fn).gethost(ip).services:
            entityname = "msploitego.MetasploitService"
            try:
                servicename = service.name
            except AttributeError:
                servicename = "NoName"
            if service.state.lower() in ["filtered", "closed"]:
                entityname = "msploitego.ClosedPort"
            else:
                if servicename in ["http","https","possible_wls","www","ncacn_http","ccproxy-http","ssl/http"]:
                    entityname = "msploitego.WebService"
                elif servicename in ["samba","netbios-ssn","smb","microsoft-ds"]:
                    entityname = "msploitego.SambaService"
                elif servicename == "ssh":
                    entityname = "msploitego.SSHService"
                elif servicename in ["dns","mdns"]:
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
                elif "tcpwrapped" in servicename:
                    entityname = "msploitego.tcpwrapped"
                elif "mysql" in servicename:
                    entityname = "msploitego.mysql"
                elif "mssql" in servicename:
                    entityname = "msploitego.mssql"
                elif "ajp" in servicename:
                    entityname = "msploitego.ajp"
                elif servicename.lower() in ["kerberos","kpasswd5","kerberos-sec"]:
                    entityname = "msploitego.kerberos"
            hostservice = mt.addEntity(entityname, "{}/{}:{}".format(servicename,service.port,service.hostid))
            hostservice.setValue = "{}/{}:{}".format(servicename,service.port,service.hostid)
            hostservice.addAdditionalFields("ip","IP Address",False,ip)
            if servicename and servicename.lower() in ["http","www","https"]:
                hostservice.addAdditionalFields("niktofile", "Nikto File", False, '')
            hostservice.addAdditionalFields("fromfile", "Source File", False, fn)
            for etag in entitytags:
                if etag in service.getTags():
                    val = service.getVal(etag)
                    hostservice.addAdditionalFields(etag, etag, False, val)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['enumservices.py',
#  '10.10.10.74',
#  'ipv4-address=10.10.10.74#ipaddress.internal=false#notecount=3#address=10.10.10.74#purpose=server#osfamily=Windows#servicecount=9#name=10.10.10.74#state=alive#vulncount=3#fromfile=/root/data/scan/hthebox/msploitdb-20180508.xml#osname=Windows 2012']
# dotransform(args)
