from pprint import pprint

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
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    servicename = mt.getVar("servicename")
    serviceid = mt.getVar("serviceid")
    hostid = mt.getVar("hostid")
    workspace = mt.getVar("workspace")

    rep = scriptrunner(port, "http-csrf", ip)
    for scriptrun in rep.hosts[0].services[0].scripts_results:
        output = scriptrun.get("output")
        csrfentity = mt.addEntity("msploitego.CSFR", scriptrun.get("id"))
        csrfentity.setValue(scriptrun.get("id"))
        csrfentity.addAdditionalFields("data", "Data", True, output)
        csrfentity.addAdditionalFields("servicename", "Service Name", True, servicename)
        csrfentity.addAdditionalFields("serviceid", "Service Id", True, serviceid)
        csrfentity.addAdditionalFields("hostid", "Host Id", True, hostid)
        csrfentity.addAdditionalFields("workspace", "Workspace", True, workspace)

    mt.returnOutput()


dotransform(sys.argv)
# dotransform(args)
