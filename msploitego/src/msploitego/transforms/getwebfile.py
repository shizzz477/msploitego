from pprint import pprint
from common.MaltegoTransform import *
from common.linuxtaskrunner import bashrunner
from common.corelib import bucketparser

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
    url = mt.getValue()
    bashlog = bashrunner("wget -qO-  {}".format(url))
    if bashlog:
        webfile = mt.addEntity("msploitego.WebFile", url.split("/")[-1])
        webfile.setValue(url.split("/")[-1])
        webfile.addAdditionalFields("details","Details",False, "".join(bashlog))
        webfile.addAdditionalFields("url", "Site URL", False, url)
        webfile.addAdditionalFields("ip", "IP Address", False, ip)
        webfile.addAdditionalFields("port", "Port", False, port)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['getwebfile.py',
#  'http://10.11.1.50:80/UPGRADE.txt',
#  'maltego.v2.value.property=http://10.11.1.50:80/UPGRADE.txt#theurl=http://10.11.1.50:80/UPGRADE.txt#dir=/UPGRADE.txt#ip=10.11.1.50#port=80']
# dotransform(args)