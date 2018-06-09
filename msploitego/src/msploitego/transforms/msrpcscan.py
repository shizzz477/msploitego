from pprint import pprint

from common.nsescriptlib import scriptrunner
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
    mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    if not hostid:
        hostid = mt.getVar("id")
    rep = scriptrunner(port, "msrpc-enum", ip)

    if rep.hosts[0].status == "up":
        for scriptrun in rep.hosts[0].services[0].scripts_results:
            popent = mt.addEntity("msploitego.RelevantInformation", "{}:{}".format(scriptrun.get("id"),hostid))
            popent.setValue("{}:{}".format(scriptrun.get("id"),hostid))
            popent.addAdditionalFields("description", "Description",False,scriptrun.get("output"))
            popent.addAdditionalFields("ip", "IP Address", False, ip)
            popent.addAdditionalFields("port", "Port", False, port)
            popent.addAdditionalFields("hostid", "Host Id", False, hostid)
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

# dotransform(sys.argv)
args = ['msrpcscan.py',
 'dcerpc/49165:512',
 'service.name=dcerpc/49165:512#port=49165#banner=367abb81-9844-35f1-ad32-98f038001003 v2.0 #properties.service= #address=10.11.1.221#ip=10.11.1.221#created_at=31/5/2018#host_id=512#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#updated_at=31/5/2018#proto=tcp#name=dcerpc#id=7062#state=open#user=msf#db=msf#info=367abb81-9844-35f1-ad32-98f038001003 v2.0 ']
dotransform(args)
