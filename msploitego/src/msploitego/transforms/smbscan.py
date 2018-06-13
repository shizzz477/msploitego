from pprint import pprint

from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *

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
    hostid = mt.getVar("host_id")
    proto = mt.getVar("proto")
    service = mt.getValue()
    rep = scriptrunner(port, "smb-os-discovery,smb-security-mode,smb-server-stats,smb-system-info", ip)
    if rep.hosts[0].status == "up":
        d = {}
        for res in rep.hosts[0].scripts_results:
            if res.get("elements"):
                d.update(res.get("elements"))

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
            if any(x in k for x in ["server","workgroup", "os", "fqdn"]):
                continue
            sambaentity.addAdditionalFields(k, k.capitalize(), False, v)
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['smbscan.py',
#  'smb/445:520',
#  'properties.samba=smb/445:520#ip=10.11.1.145#service.name=smb/445:520#machinename=HELPDESK#banner.text=Windows 2008 Service Pack 1 (Unknown)#info=Windows 2008 Service Pack 1 (Unknown)#name=smb#proto=tcp#created_at=11/3/2018#updated_at=11/6/2018#id=6837#state=open#address=10.11.1.145#host_id=520#port=445#user=msf#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#db=msf']
# dotransform(args)
