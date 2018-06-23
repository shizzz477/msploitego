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
    hostid = mt.getVar("hostid")
    rep = scriptrunner(port, "smtp-enum-users", ip)
    if rep:
        for res in rep.hosts[0].services[0].scripts_results:
            output = res.get("output")
            for username in output.split(","):
                username = username.strip().lstrip()
                userentity = mt.addEntity("maltego.Alias", username)
                userentity.setValue(username)
                userentity.addAdditionalFields("sourceip", "Source IP", False, ip)
                userentity.addAdditionalFields("sourceport", "Source Port", False, port)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()


dotransform(sys.argv)
# dotransform(args)
