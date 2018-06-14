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
    rep = scriptrunner(port, "http-robots.txt", ip)

    if rep:
        for scriptrun in rep.hosts[0].services[0].scripts_results:
            output = scriptrun.get("output")
            for line in output.split("\n"):
                if line.lstrip()[0] == "/":
                    for d in line.lstrip().strip().split():
                        webdirentity = mt.addEntity("maltego.WebDir", d)
                        webdirentity.setValue(d)
                        webdirentity.addAdditionalFields("ip", "IP Address", False, ip)
                        webdirentity.addAdditionalFields("port", "Port", False, port)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)
