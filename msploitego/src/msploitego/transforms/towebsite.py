from pprint import pprint

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

    website = mt.addEntity("maltego.Website", "http://{}:{}".format(ip,port))
    website.setValue("http://{}:{}".format(ip,port))
    website.addAdditionalFields("url", "Site URL", False, "http://{}:{}".format(ip,port))
    website.addAdditionalFields("ip", "IP Address", False, ip)
    website.addAdditionalFields("port", "Port", False, port)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# dotransform(args)
