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
    hostid = mt.getVar("hostid")
    rep = scriptrunner(port, "dns-nsid", ip, args="-sSU")

    if rep:
        for res in rep.hosts[0].services[0].scripts_results:
            did = res.get("id")
            if id:
                dnsnsid = mt.addEntity("msploitego.dnsnsid", "{}:{}".format(did,hostid))
                dnsnsid.setValue("{}:{}".format(did,hostid))
    else:
        mt.addUIMessage("host is either down or not responding in this port")

    mt.returnOutput()

dotransform(sys.argv)
