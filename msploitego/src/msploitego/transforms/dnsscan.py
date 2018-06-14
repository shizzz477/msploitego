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
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    servicename = mt.getVar("servicename")
    serviceid = mt.getVar("serviceid")
    hostid = mt.getVar("hostid")
    workspace = mt.getVar("workspace")
    rep = scriptrunner("53,5353", "dns-random-srcport,dns-random-txid,dns-recursion,dns-service-discovery", ip, args="-sU")

    if rep:
        for service in rep.hosts[0].services:
            for res in service.scripts_results:
                output = res.get("output")
                dnsinfo = mt.addEntity("msploitego.DNSInformation", res.get("id"))
                dnsinfo.setValue("{}:{}".format(res.get("id"),hostid))
                dnsinfo.addAdditionalFields("data", "Data", True, output)
                dnsinfo.addAdditionalFields("servicename", "Service Name", True, servicename)
                dnsinfo.addAdditionalFields("serviceid", "Service Id", True, serviceid)
                dnsinfo.addAdditionalFields("hostid", "Host Id", True, hostid)
                dnsinfo.addAdditionalFields("workspace", "Workspace", True, workspace)
                dnsinfo.addAdditionalFields("ip", "IP Address", False, ip)
                dnsinfo.addAdditionalFields("port", "Port", False, str(service.port))
                dnsinfo.addAdditionalFields("protocol", "Protocol", False, service.protocol)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()

dotransform(sys.argv)
# args = ['dnsscan.py',
#  'domain/53:800',
#  'service.name=domain/53:800#port=53#banner=ISC BIND 9.9.5-3ubuntu0.14 Ubuntu Linux#properties.service= #workspace=space2#ip=10.10.10.79#hostid=800#created_at=16/5/2018#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#updated_at=16/5/2018#proto=tcp#servicename=domain#state=open#serviceid=7688#user=msf#db=msf#info=ISC BIND 9.9.5-3ubuntu0.14 Ubuntu Linux#workspaceid=19']
# dotransform(args)
