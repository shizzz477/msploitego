import re
from pprint import pprint

from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *
import sys

from common.corelib import bucketparser

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    global nmap_proc
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")

    rep = scriptrunner(port, "http-comments-displayer", ip)
    for scriptrun in rep.hosts[0].services[0].scripts_results:
        regex = re.compile("^\s+Path:")
        results = bucketparser(regex,scriptrun.get("output").split("\n"))
        for res in results:
            k,v = res.get("Header").split(":",1)
            commententity = mt.addEntity("msploitego.SourceCodeComment", v)
            commententity.setValue(v)
            commententity.addAdditionalFields("comment", "Comment", False, "\n".join(res.get("Details")))
            commententity.addAdditionalFields("linenumber", "Line Number", False, res.get("Line number"))
            commententity.addAdditionalFields("path", "Path", False, v)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# dotransform(args)
