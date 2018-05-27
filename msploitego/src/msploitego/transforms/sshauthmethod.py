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
    rep = scriptrunner(port, "ssh-auth-methods", ip)

    for scriptrun in rep.hosts[0].services[0].scripts_results:
        output = scriptrun.get("output")
        elements = scriptrun.get("elements").get("Supported authentication methods").get(None)
        for elem in elements:
            authmethod = mt.addEntity("msploitego.SSHAuthenticationMethod", elem)
            authmethod.setValue(elem)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['sshauthmethod.py',
#  'ssh/22:265',
#  'properties.metasploitservice=ssh/22:265#info=OpenSSH 7.4p1 Debian 10+deb9u2 protocol 2.0#name=ssh#proto=tcp#hostid=265#service.name=80/Apache 9#port=22#banner=Apache 9#properties.service= #ip=10.10.10.55#state=open#fromfile=/root/data/scan/hthebox/msploitdb-20180508.xml']
# dotransform(args)
