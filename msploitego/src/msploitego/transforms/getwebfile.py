from pprint import pprint
from common.MaltegoTransform import *
from common.linuxtaskrunner import bashrunner
import tempfile

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
        f = tempfile.NamedTemporaryFile(delete=False)
        f.file.write(details)
        f.file.close()
        webfile.addAdditionalFields("localfile","Local File",False, f.name)
        webfile.addAdditionalFields("url", "Site URL", False, url)
        webfile.addAdditionalFields("ip", "IP Address", False, ip)
        webfile.addAdditionalFields("port", "Port", False, port)
    mt.returnOutput()


dotransform(sys.argv)
# dotransform(args)