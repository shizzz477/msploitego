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
    servicename = mt.getVar("servicename")
    serviceid = mt.getVar("serviceid")
    hostid = mt.getVar("hostid")
    workspace = mt.getVar("workspace")
    rep = scriptrunner(port, "http-security-headers", ip)

    if rep:
        for res in rep.hosts[0].services[0].scripts_results:
            output = res.get("output").strip()
            if output:
                secheader = mt.addEntity("msploitego.httpsecureheaders", "{}:{}".format(res.get("id"),hostid))
                secheader.setValue("{}:{}".format(res.get("id"),hostid))
                secheader.addAdditionalFields("details", "Details", False, output)
                secheader.addAdditionalFields("servicename", "Service Name", True, servicename)
                secheader.addAdditionalFields("serviceid", "Service Id", True, serviceid)
                secheader.addAdditionalFields("hostid", "Host Id", True, hostid)
                secheader.addAdditionalFields("workspace", "Workspace", True, workspace)
                secheader.addAdditionalFields("ip", "IP Address", False, ip)
                secheader.addAdditionalFields("port", "Port", False, port)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
