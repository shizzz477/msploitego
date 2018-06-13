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
# args = ['httpcsrf.py',
#  'http/80:531',
#  'properties.metasploitservice=http/80:531#info=Microsoft-IIS/6.0#proto=tcp#hostid=531#service.name=http/80:531#port=80#banner=Microsoft-IIS/6.0#properties.service= #ip=10.11.1.10#machinename=10.11.1.10#servicename=http#created_at=24/2/2018#updated_at=11/6/2018#workspaceid=18#state=open#serviceid=6877#workspace=default#user=msf#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#db=msf']
# dotransform(args)
