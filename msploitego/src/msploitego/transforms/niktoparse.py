from common.MaltegoTransform import *
from common.niktolib import NiktoReport
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
            det = mt.addEntity("msploitego.niktodetail", "{}:{}".format(d.description,hostid))
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
# args = ['httpvulnscan.py',
#  'http/80:535',
# 'properties.metasploitservice=http/80:535#info=Apache httpd 2.0.40 (Red Hat Linux)#proto=tcp#hostid=535#service.name=http/80:535#port=80#banner=Apache httpd 2.0.40 (Red Hat Linux)#properties.service= #ip=10.11.1.115#machinename=10.11.1.115#servicename=http#created_at=24/2/2018#updated_at=24/2/2018#workspaceid=18#state=open#serviceid=6888#workspace=default#user=msf#niktofile=/root/data/oscp_prep/scan_pack/nikto/10.11.1.115-80.xml#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#db=msf']
# dotransform(args)