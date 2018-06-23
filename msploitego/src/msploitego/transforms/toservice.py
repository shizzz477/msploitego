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
    mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    diry = mt.getValue()

    # website = mt.addEntity("maltego.URL", "http://{}:{}{}".format(ip,port,diry))
    # website.setValue("http://{}:{}{}".format(ip,port,diry))
    # website.addAdditionalFields("dir", "Directory", False, diry)
    # website.addAdditionalFields("url", "URL", False, "http://{}:{}{}".format(ip,port,diry))
    # website.addAdditionalFields("ip", "IP Address", False, ip)
    # website.addAdditionalFields("port", "Port", False, port)
    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)
