from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *
import sys
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
    hostid = mt.getVar("hostid")
    port = mt.getVar("port")
    ip = mt.getVar("ip")
    rep = scriptrunner(port, "http-security-headers", ip)

    if rep:
        for res in rep.hosts[0].services[0].scripts_results:
            output = res.get("output").strip()
            if output:
                secheader = mt.addEntity("msploitego.httpsecureheaders", "{}:{}".format(res.get("id"),hostid))
                secheader.setValue("{}:{}".format(res.get("id"),hostid))
                secheader.addAdditionalFields("details", "Details", False, output)
                inheritvalues(secheader, mt)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
