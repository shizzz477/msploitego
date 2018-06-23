from pprint import pprint

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
    path = mt.getVar("uri")
    namelink = mt.getVar("namelink")

    urlent = mt.addEntity("msploitego.SiteURL", namelink)
    urlent.setValue(namelink)
    urlent.addAdditionalFields("ip", "IP Address", False, ip)
    urlent.addAdditionalFields("port", "Port", False, port)
    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)
