from pprint import pprint
from common.MaltegoTransform import *
from common.linuxtaskrunner import bashrunner

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
    body = mt.getVar("body")
    url = mt.getValue()
    details = None
    if body:
        details = body
    else:
        bashlog = bashrunner("wget -qO-  {}".format(url))
        if bashlog:
            details = "".join(bashlog)
    if details:
        webfile = mt.addEntity("msploitego.WebFile", url)
        webfile.setValue(url)
        webfile.addAdditionalFields("details","Details",False, details)
        webfile.addAdditionalFields("url", "Site URL", False, url)
        webfile.addAdditionalFields("ip", "IP Address", False, ip)
        webfile.addAdditionalFields("port", "Port", False, port)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# dotransform(args)