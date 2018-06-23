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
    hostid = mt.getVar("hostid")
    if not hostid:
        hostid = mt.getVar("id")
    rep = scriptrunner(port, "msrpc-enum", ip)

    if rep:
        for scriptrun in rep.hosts[0].services[0].scripts_results:
            popent = mt.addEntity("msploitego.RelevantInformation", "{}:{}".format(scriptrun.get("id"),hostid))
            popent.setValue("{}:{}".format(scriptrun.get("id"),hostid))
            popent.addAdditionalFields("description", "Description",False,scriptrun.get("output"))
            popent.addAdditionalFields("ip", "IP Address", False, ip)
            popent.addAdditionalFields("port", "Port", False, port)
            popent.addAdditionalFields("hostid", "Host Id", False, hostid)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()

dotransform(sys.argv)
