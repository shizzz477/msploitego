from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *
import sys

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    global nmap_proc
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    rep = scriptrunner(port, "http-security-headers", ip)

    for scriptrun in rep.hosts[0].services[0].scripts_results:
        output = scriptrun.get("output")
        lines = output.split("\n")
        for line in lines:
            if not line.strip():
                lines.remove(line)
        secheader = mt.addEntity("msploitego.httpsecureheaders", output)
        secheader.setValue(output[0:25])
        secheader.addAdditionalFields("details", "Details", False, output)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# dotransform(args)
