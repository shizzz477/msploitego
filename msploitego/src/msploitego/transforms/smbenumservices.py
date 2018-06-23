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
    rep = scriptrunner(port, "smb-enum-services", ip)

    if rep:
        for res in rep.hosts[0].services[0].scripts_results:
            output = res.get("output").split("\n")
            regex = re.compile("^\s\s[a-zA-Z0-9_.-]+")
            bucket = bucketparser(regex,output)
            for item in bucket:
                serviceent = mt.addEntity("maltego.Service", "{}:{}".format(item.get("Header"),hostid))
                serviceent.setValue("{}:{}".format(item.get("Header"),hostid))
                serviceent.addAdditionalFields("displayname", "Service Name", False, item.get("Display_name"))
                serviceent.addAdditionalFields("ip", "IP Address", False, ip)
                serviceent.addAdditionalFields("port", "Port", False, port)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)
