from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *
from deprecated import deprecated

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

@deprecated("use sshscan transform")
def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    rep = scriptrunner(port, "ssh-auth-methods", ip)
    if rep:
        for scriptrun in rep.hosts[0].services[0].scripts_results:
            infoentity = mt.addEntity("msploitego.SSHAuthenticationMethod", "{}:{}".format(scriptrun.get("id"), hostid))
            infoentity.setValue("{}:{}".format(scriptrun.get("id"), hostid))
            infoentity.addAdditionalFields("description", "Description", False, scriptrun.get("output"))
            infoentity.addAdditionalFields("ip", "IP Address", False, ip)
            infoentity.addAdditionalFields("port", "Port", False, port)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()


dotransform(sys.argv)
# dotransform(args)
