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
    rep = scriptrunner(port, "smb-mbenum", ip)

    if rep:
        for res in rep.hosts[0].scripts_results:
            output = res.get("output").split("\n")
            regex = re.compile("^\s{2}\w")
            bucket = bucketparser(regex,output,sep=" ")
            for item in bucket:
                header = item.get("Header")
                shareentity = mt.addEntity("msploitego.WindowsMasterBrowser", "{}:{}".format(header,hostid))
                shareentity.setValue("{}:{}".format(header,hostid))
                shareentity.addAdditionalFields("ip", "IP Address", False, ip)
                shareentity.addAdditionalFields("port", "Port", False, port)
                for k,v in item.items():
                    if k == "Header" or k == "Details":
                        continue
                    shareentity.addAdditionalFields(k.lower(), k, False, "{}/{}".format(k,v))
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)
