from pprint import pprint

from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *
from common.corelib import bucketparser

import re

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    proto = mt.getVar("proto")
    service = mt.getValue()
    rep = scriptrunner(port, "smb-os-discovery,smb-security-mode,smb-server-stats,smb-system-info", ip)
    if rep.hosts[0].status == "up":
        d = {}
        for res in rep.hosts[0].scripts_results:
            elems = res.get("elements")
            for k,v in elems.items():
                if v and v.strip():
                    d.update({k:v})
        server = d.get("server").split("\\")[0]
        workgroup = d.get("workgroup").split("\\")[0]
        sambaentity = mt.addEntity("msploitego.SambaServer", "{}:{}".format(server,workgroup))
        sambaentity.setValue("{}:{}".format(server,workgroup))
        sambaentity.addAdditionalFields("ip", "IP Address", False, ip)
        sambaentity.addAdditionalFields("port", "Port", False, port)
        sambaentity.addAdditionalFields("server", "Server", False, server)
        sambaentity.addAdditionalFields("workgroup", "Workgroup", False, workgroup)
        sambaentity.addAdditionalFields("hostid", "Hostid", False, hostid)
        sambaentity.addAdditionalFields("info", "Info", False, d.get("os"))
        sambaentity.addAdditionalFields("name", "Name", False, d.get("fqdn"))
        sambaentity.addAdditionalFields("banner.text", "Service Banner", False, d.get("os"))
        sambaentity.addAdditionalFields("service.name", "Description", False, service)
        sambaentity.addAdditionalFields("properties.service", "Service", False, service)
        sambaentity.addAdditionalFields("proto", "Protocol", False, proto)
        for k,v in d.items():
            if any(x in k for x in ["server","workgroup"]):
                continue
            sambaentity.addAdditionalFields(k, k.capitalize(), False, v)
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['smbscan.py',
#  'microsoft-ds/445:550',
#  'properties.metasploitservice=microsoft-ds/445:550#info=Microsoft Windows 7 - 10 microsoft-ds workgroup: WORKGROUP#name=microsoft-ds#proto=tcp#hostid=550#service.name=microsoft-ds#port=445#banner=Microsoft Windows 7 - 10 microsoft-ds workgroup: WORKGROUP#properties.service= #ip=10.11.1.73#fromfile=/root/data/report_pack/msploitdb20180601.xml#state=open']
#
# dotransform(args)
