from pprint import pprint

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
    rep = scriptrunner(port, "http-sitemap-generator", ip)

    if rep:
        for res in rep.hosts[0].services[0].scripts_results:
            output = res.get("output").strip().split("\n")
            regex = re.compile("^\s{4}/")
            for line in output:
                if regex.match(line):
                    webdir = mt.addEntity("maltego.WebDir", "{}:{}".format(line.strip().lstrip(),hostid))
                    webdir.setValue("{}:{}".format(line.strip().lstrip(),hostid))
                    webdir.addAdditionalFields("ip", "IP Address", False, ip)
                    webdir.addAdditionalFields("port", "Port", False, port)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()
    

dotransform(sys.argv)
