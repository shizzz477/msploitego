from pprint import pprint
from datetime import datetime
from common.MaltegoTransform import *
from common.postgresdb import MsploitPostgres
import sys
from common.servicefactory import getserviceentity, getosentity
import os.path

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

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getValue()
    mac = mt.getVar("mac")
    machinename = mt.getVar("name")
    os_family = mt.getVar("os_family")
    os_name = mt.getVar("os_name")
    os_sp = mt.getVar("os_sp")
    hostid = mt.getVar("id")
    if not hostid:
        hostid = mt.getVar("hostid")
    db = mt.getVar("db")
    user = mt.getVar("user")
    password = mt.getVar("password").replace("\\", "")
    # workspace = mt.getVar("workspace")
    mpost = MsploitPostgres(user, password, db)
    for service in mpost.getServices(hostid):
        entityname = getserviceentity(service)
        servicename = service.get("servicename")
        if not servicename:
            servicename = "unknown"
        hostservice = mt.addEntity(entityname, "{}/{}:{}".format(servicename, service.get("port"), hostid))
        hostservice.setValue("{}/{}:{}".format(servicename, service.get("port"), hostid))
        hostservice.addAdditionalFields("ip", "IP Address", True, ip)
        hostservice.addAdditionalFields("service.name", "Description", True, "{}/{}:{}".format(servicename, service.get("port"), hostid))
        if machinename:
            hostservice.addAdditionalFields("machinename", "Machine Name", True, machinename)
        if service.get("info"):
            hostservice.addAdditionalFields("banner.text", "Service Banner", True, service.get("info"))
        else:
            hostservice.addAdditionalFields("banner.text", "Service Banner", True, "")

        if any(x in servicename for x in webservices):
            niktofile = "/root/nikto/{}-{}.xml".format(ip,service.get("port"))
            if not os.path.exists(niktofile):
                niktofile = ""
            hostservice.addAdditionalFields("niktofile", "Nikto File", True, niktofile)
        elif any(x in servicename for x in sambaservices):
            enum4file = "/root/enum4/{}-enum4.txt".format(ip)
            if not os.path.exists(enum4file):
                enum4file = ""
            hostservice.addAdditionalFields("enum4linux", "enum4linux File", True, enum4file)
        for k,v in service.items():
            if isinstance(v,datetime):
                hostservice.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                hostservice.addAdditionalFields(k, k.capitalize(), False, str(v))
        hostservice.addAdditionalFields("user", "User", False, user)
        hostservice.addAdditionalFields("password", "Password", False, password)
        hostservice.addAdditionalFields("db", "db", False, db)
    if mac:
        macentity = mt.addEntity("maltego.MacAddress", mac)
        macentity.setValue(mac)
        macentity.addAdditionalFields("ip", "IP Address", True, ip)
    # if machinename and re.match("^[a-zA-z]+", machinename):
    if machinename:
        hostentity = mt.addEntity("msploitego.Hostname", machinename)
        hostentity.setValue(machinename)
        hostentity.addAdditionalFields("ip", "IP Address", True, ip)
    osentityname, osdescription = getosentity(os_family,os_name)
    if os_sp:
        osdescription += " {}".format(os_sp)
    osentity = mt.addEntity(osentityname, osdescription)
    osentity.setValue(osdescription)
    osentity.addAdditionalFields("ip", "IP Address", True, ip)

    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)