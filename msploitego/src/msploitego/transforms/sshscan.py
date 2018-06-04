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
    rep = scriptrunner(port, "ssh-auth-methods,ssh-hostkey", ip, scriptargs="ssh_hostkey=all")
    if rep.hosts[0].status == "up":
        for scriptrun in rep.hosts[0].services[0].scripts_results:
            infoentity = mt.addEntity("msploitego.RelevantInformation", "{}:{}".format(scriptrun.get("id"), hostid))
            infoentity.setValue("{}:{}".format(scriptrun.get("id"), hostid))
            infoentity.addAdditionalFields("description", "Description", False, scriptrun.get("output"))
            infoentity.addAdditionalFields("ip", "IP Address", False, ip)
            infoentity.addAdditionalFields("port", "Port", False, port)
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['sshauthmethod.py',
#  'ssh/22:265',
#  'properties.metasploitservice=ssh/22:265#info=OpenSSH 7.4p1 Debian 10+deb9u2 protocol 2.0#name=ssh#proto=tcp#hostid=265#service.name=80/Apache 9#port=22#banner=Apache 9#properties.service= #ip=10.11.1.234#state=open#fromfile=/root/data/scan/hthebox/msploitdb-20180508.xml']
# dotransform(args)
