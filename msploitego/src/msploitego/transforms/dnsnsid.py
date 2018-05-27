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
    hostid = mt.getVar("hostid")
    rep = scriptrunner(port, "dns-nsid", ip, args="-sSU")

    for res in rep.hosts[0].services[0].scripts_results:
        id = res.get("id")
        if id:
            dnsnsid = mt.addEntity("msploitego.dnsnsid", "{}:{}".format(id,hostid))
            dnsnsid.setValue("{}:{}".format(id,hostid))

    mt.returnOutput()
    mt.addUIMessage("completed!")

# dotransform(sys.argv)
args = ['dnsnsid.py',
 'dns/53:259',
 'properties.metasploitservice=dns/53:259#info=Microsoft DNS 6.1.7601 (1DB15D39) Windows Server 2008 R2 SP1#name=dns#proto=udp#hostid=259#service.name=80/Apache 9#port=53#banner=Apache 9#properties.service= #ip=10.10.10.71#state=open#fromfile=/root/data/scan/hthebox/msploitdb20180517.xml']
dotransform(args)
