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
    servicename = mt.getVar("servicename")
    serviceid = mt.getVar("serviceid")
    hostid = mt.getVar("hostid")
    workspace = mt.getVar("workspace")

    website = mt.addEntity("maltego.Website", "http://{}:{}".format(ip,port))
    website.setValue("http://{}:{}".format(ip,port))
    website.addAdditionalFields("url", "Site URL", False, "http://{}:{}".format(ip,port))
    website.addAdditionalFields("ip", "IP Address", False, ip)
    website.addAdditionalFields("port", "Port", False, port)
    website.addAdditionalFields("servicename", "Service Name", True, servicename)
    website.addAdditionalFields("serviceid", "Service Id", True, serviceid)
    website.addAdditionalFields("hostid", "Host Id", True, hostid)
    website.addAdditionalFields("workspace", "Workspace", True, workspace)

    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
