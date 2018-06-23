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
    rep = scriptrunner(port, "smb-enum-groups", ip)

    if rep:
        for res in rep.hosts[0].scripts_results:
            output = res.get("output").strip().split("\n")
            for item in output:
                d = item.split()
                groupentity = mt.addEntity("msploitego.UserGroup", d[0])
                groupentity.setValue(d[0])
                groupentity.addAdditionalFields("groupname", "Group Name", False, d[0])
                groupentity.addAdditionalFields("details", "Details", False, " ".join(d[1::]))
                groupentity.addAdditionalFields("ip", "IP Address", False, ip)
                groupentity.addAdditionalFields("port", "Port", False, port)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)
