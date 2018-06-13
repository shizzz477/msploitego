from pprint import pprint

from common.MaltegoTransform import *

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
# args = ['towebsite.py',
#  'http/80:544',
#  'properties.metasploitservice=http/80:544#info=Apache httpd 2.2.11 (Ubuntu) PHP/5.2.6-3ubuntu4.4 with Suhosin-Patch#proto=tcp#hostid=544#service.name=http/80:544#port=80#banner=Apache httpd 2.2.11 (Ubuntu) PHP/5.2.6-3ubuntu4.4 with Suhosin-Patch#properties.service= #ip=10.11.1.251#machinename=10.11.1.251#servicename=http#created_at=24/2/2018#updated_at=24/2/2018#workspaceid=18#state=open#serviceid=6936#workspace=default#user=msf#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#db=msf']
# dotransform(args)
