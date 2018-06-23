import re
from pprint import pprint

from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *
from common.corelib import bucketparser

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
    rep = scriptrunner(port, "rdp-vuln-ms12-020", ip)

    if rep:
        for res in rep.hosts[0].services[0].scripts_results:
            regex = re.compile("\s{2}[A-Za-z]+")
            output = res.get("output").split("\n")
            results = bucketparser(regex,output)
            for res in results:
                if res.get("Header") == "VULNERABLE":
                    continue
                vulnentity = mt.addEntity("msploitego.RDPVulnerability", "{}:{}".format(res.get("Header"),hostid))
                vulnentity.setValue("{}:{}".format(res.get("Header"),hostid))
                vulnentity.addAdditionalFields("ip", "IP Address", False, ip)
                vulnentity.addAdditionalFields("port", "Port", False, port)
                for k,v in res.items():
                    if k == "Details":
                        vulnentity.addAdditionalFields("details", k, False, "\n".join(v))
                    else:
                        if v and v.strip():
                            vulnentity.addAdditionalFields(k, k.capitalize(), False, v)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
