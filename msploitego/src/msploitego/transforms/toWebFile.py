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
    path = mt.getVar("uri")
    namelink = mt.getVar("namelink")

    urlent = mt.addEntity("msploitego.WebFile", namelink)
    urlent.setValue(namelink)
    urlent.addAdditionalFields("ip", "IP Address", False, ip)
    urlent.addAdditionalFields("port", "Port", False, port)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['/root/transforms/toURL.py',
#  '/files/: Directory indexing found.',
#  'properties.niktodetail=/files/: Directory indexing found.#description=/files/: Directory indexing found.#iplink=https://10.11.1.35:443/files/#namelink=https://10.11.1.35:443/files/#uri=/files/#ip=10.11.1.35#port=443']
# dotransform(args)
