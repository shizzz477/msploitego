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
    if not hostid:
        hostid = mt.getVar("id")
    rep = scriptrunner(port, "smtp-commands,smtp-enum-users,smtp-open-relay,smtp-vuln-cve2011-1764", ip)

    if rep.hosts[0].status == "up":
        for scriptrun in rep.hosts[0].services[0].scripts_results:
            infoentity = mt.addEntity("msploitego.RelevantInformation", "{}:{}".format(scriptrun.get("id"),hostid))
            infoentity.setValue("{}:{}".format(scriptrun.get("id"),hostid))
            infoentity.addAdditionalFields("description", "Description",False,scriptrun.get("output"))
            infoentity.addAdditionalFields("ip", "IP Address", False, ip)
            infoentity.addAdditionalFields("port", "Port", False, port)
            infoentity.addAdditionalFields("hostid", "Host Id", False, hostid)
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['smtpenumusers.py',
#  'smtp/25:298',
#  'properties.metasploitservice=smtp/25:298#info=JAMES smtpd 2.3.2#name=smtp#proto=tcp#hostid=298#service.name=80/Apache 9#port=25#banner=Apache 9#properties.service= #ip=10.11.1.227#state=open#fromfile=/root/data/scan/hthebox/msploitdb20180517.xml']
# dotransform(args)
