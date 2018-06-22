from pprint import pprint

from common.MaltegoTransform import *
from common.niktolib import NiktoReport
import sys
import os.path

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
    # mt.debug(pprint(sys.argv))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    servicename = mt.getVar("servicename")
    serviceid = mt.getVar("serviceid")
    hostid = mt.getVar("hostid")
    workspace = mt.getVar("workspace")
    fn = mt.getVar("niktofile")
    if not fn:
        mt.addException("Nikto file is either not attached or does not exist")
        mt.returnOutput()
    else:
        nr = NiktoReport(fn)
        for d in nr.details:
            try:
                det = mt.addEntity("msploitego.niktodetail", "{}:{}".format(d.description,hostid))
            except Exception:
                continue
            det.setValue("{}:{}".format(d.description,hostid))
            det.addAdditionalFields("description","Description",False,d.description)
            det.addAdditionalFields("iplink", "IP Link", False, d.iplink)
            det.addAdditionalFields("namelink", "Name Link", False, d.namelink)
            det.addAdditionalFields("uri", "URI", False, d.uri)
            det.addAdditionalFields("servicename", "Service Name", True, servicename)
            det.addAdditionalFields("serviceid", "Service Id", True, serviceid)
            det.addAdditionalFields("hostid", "Host Id", True, hostid)
            det.addAdditionalFields("workspace", "Workspace", True, workspace)
            det.addAdditionalFields("ip", "IP Address", False, ip)
            det.addAdditionalFields("port", "Port", False, port)

        mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)