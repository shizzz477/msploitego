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
    rep = scriptrunner("53,5353", "dns-random-srcport,dns-random-txid,dns-recursion,dns-service-discovery", ip, args="-sU")

    if rep:
        for service in rep.hosts[0].services:
            for res in service.scripts_results:
                output = res.get("output")
                dnsinfo = mt.addEntity("msploitego.DNSInformation", "{}:{}".format(res.get("id"),hostid))
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
# dotransform(args)
