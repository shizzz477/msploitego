from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *
from common.corelib import bucketparser

import re

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
    rep = scriptrunner(port, "smb-enum-users", ip)

    if rep:
        for res in rep.hosts[0].scripts_results:
            output = res.get("output").strip().split("\n")
            regex = re.compile("^[\sa-zA-Z0-9_.-]+\\\\")
            bucket = bucketparser(regex,output)
            for item in bucket:
                userentity = mt.addEntity("msploitego.SambaUser", item.get("Header"))
                userentity.setValue(item.get("Header"))
                userentity.addAdditionalFields("ip", "IP Address", False, ip)
                userentity.addAdditionalFields("port", "Port", False, port)
                for k,v in item.items():
                    userentity.addAdditionalFields(k, k.capitalize(), False, v.strip())
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)
