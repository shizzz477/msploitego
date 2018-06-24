from pprint import pprint

from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *
from common.corelib import inheritvalues

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
    hostid = mt.getVar("hostid")
    rep = scriptrunner(port, "http-apache-negotiation,http-apache-server-status,http-vuln-cve2011-3192,http-vuln-cve2011-3368,http-vuln-cve2017-5638 ", ip)

    if rep:
        for res in rep.hosts[0].services[0].scripts_results:
            apachevuln = mt.addEntity("msploitego.ApacheVulnerability", "{}:{}".format(res.get("id"),hostid))
            apachevuln.setValue("{}:{}".format(res.get("id"),hostid))
            apachevuln.addAdditionalFields(ip, "IP Address", False, ip)
            apachevuln.addAdditionalFields(hostid, "Host Id", False, hostid)
            inheritvalues(apachevuln,mt.values)
            for k,v in res.get("elements").items():
                if isinstance(v,dict):
                    apachevuln.addAdditionalFields("vuln", "Vuln", False, k)
                    for key, value in v.items():
                        if value and value.strip():
                            apachevuln.addAdditionalFields(key, key.capitalize(), False, value.strip())
                elif v and v.strip():
                    apachevuln.addAdditionalFields(k, k.capitalize(), False, v.strip())
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
