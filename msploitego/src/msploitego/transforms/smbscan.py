from pprint import pprint

from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
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
    if rep:
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
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)
