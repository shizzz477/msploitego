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
    rep = scriptrunner(port, "http-phpself-xss,http-stored-xss", ip)

    if rep.hosts[0].status == "up":
        for res in rep.hosts[0].services[0].scripts_results:
            if res.get("elements"):
                for key, elem in res.get("elements").items():
                    vulnentity = mt.addEntity("msploitego.XSSVulnerability", elem.get("title"))
                    vulnentity.setValue(res.get("title"))
                    vulnentity.addAdditionalFields("vulnid", "Vuln ID", False, res.get("id"))
                    vulnentity.addAdditionalFields("description", "Description", False, res.get("output"))
                    vulnentity.addAdditionalFields("ip", "IP Address", False, ip)
                    vulnentity.addAdditionalFields("port", "Port", False, port)
                    for k,v in elem.items():
                        if v.strip():
                            vulnentity.addAdditionalFields(k, k.capitalize(), False, v)
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# dotransform(args)
