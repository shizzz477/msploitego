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
    hostid = mt.getVar("hostid")
    workspace = mt.getVar("workspace")
    workspaceid = mt.getVar("workspaceid")
    servicename= mt.getVar("servicename")
    serviceid = mt.getVar("serviceid")

    rep = scriptrunner(port, "http-apache-negotiation,http-apache-server-status,http-vuln-cve2011-3192,http-vuln-cve2011-3368,http-vuln-cve2017-5638 ", ip)

    if rep:
        for res in rep.hosts[0].services[0].scripts_results:
            cve = res.get("elements").popitem()
            if len(cve) > 0:
                apachevuln = mt.addEntity("msploitego.ApacheVulnerability", "{}:{}".format(cve[0],hostid))
                apachevuln.setValue("{}:{}".format(cve[0],hostid))
                if isinstance(cve[1],dict):
                    details = cve[1]
                    for key,value in details.items():
                        if value and value.strip():
                            apachevuln.addAdditionalFields(key, key, False, value.strip())
                apachevuln.addAdditionalFields(ip, "IP Address", False, ip)
                apachevuln.addAdditionalFields(hostid, "Host Id", False, hostid)
                apachevuln.addAdditionalFields(workspace, "Workspace", False, workspace)
                apachevuln.addAdditionalFields(workspaceid, "Workspace Id", False, workspaceid)
                apachevuln.addAdditionalFields(servicename, "Servicename", False, servicename)
                apachevuln.addAdditionalFields(serviceid, "Service Id", False, serviceid)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
