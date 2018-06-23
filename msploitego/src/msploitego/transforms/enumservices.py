import re
from pprint import pprint

from common.msploitdb import MetasploitXML
from common.MaltegoTransform import *
import sys

from common.servicefactory import getserviceentity, getosentity

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
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
        for service in host.services:
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
                entityname = getserviceentity(service)

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
            osentityname, osdescription = getosentity(osfamily, osname)
            # osentityname = "msploitego.OperatingSystem"
            osentity = mt.addEntity(osentityname, osdescription)
            osentity.setValue(osdescription)
            osentity.addAdditionalFields("ip", "IP Address", True, ip)

    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)
