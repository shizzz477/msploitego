from pprint import pprint

from common.nsescriptlib import scriptrunner
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
    rep = scriptrunner(port, "http-sitemap-generator", ip)

    if rep:
        for res in rep.hosts[0].services[0].scripts_results:
            output = res.get("output")
            webdir = mt.addEntity("msploitego.WebDirectoryInfo", "{}:{}:{}".format(res.get("id"),hostid,port))
            webdir.setValue("{}:{}:{}".format(res.get("id"),hostid,port))
            webdir.addAdditionalFields("data", "Data", True, output)
            webdir.addAdditionalFields("servicename", "Service Name", True, servicename)
            webdir.addAdditionalFields("serviceid", "Service Id", True, serviceid)
            webdir.addAdditionalFields("hostid", "Host Id", True, hostid)
            webdir.addAdditionalFields("workspace", "Workspace", True, workspace)
            webdir.addAdditionalFields("ip", "IP Address", False, ip)
            webdir.addAdditionalFields("port", "Port", False, port)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
