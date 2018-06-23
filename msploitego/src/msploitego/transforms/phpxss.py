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
    servicename = mt.getVar("servicename")
    serviceid = mt.getVar("serviceid")
    hostid = mt.getVar("hostid")
    workspace = mt.getVar("workspace")
    rep = scriptrunner(port, "http-phpself-xss,http-stored-xss", ip)

    if rep:
        for res in rep.hosts[0].services[0].scripts_results:
            vulnentity = mt.addEntity("msploitego.XSSVulnerability", "{}:{}".format(res.get("id"),hostid))
            vulnentity.setValue("{}:{}".format(res.get("id"),hostid))
            vulnentity.addAdditionalFields("vulnid", "Vuln ID", False, res.get("id"))
            vulnentity.addAdditionalFields("description", "Description", False, res.get("output"))
            vulnentity.addAdditionalFields("ip", "IP Address", False, ip)
            vulnentity.addAdditionalFields("port", "Port", False, port)
            vulnentity.addAdditionalFields("servicename", "Service Name", True, servicename)
            vulnentity.addAdditionalFields("serviceid", "Service Id", True, serviceid)
            vulnentity.addAdditionalFields("hostid", "Host Id", True, hostid)
            vulnentity.addAdditionalFields("workspace", "Workspace", True, workspace)
            if res.get("elements"):
                for k,v in res.get("elements").items():
                    if v and v.strip():
                        vulnentity.addAdditionalFields(k, k.capitalize(), False, v)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
