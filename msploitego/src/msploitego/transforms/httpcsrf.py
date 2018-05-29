from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *
import sys

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
    name = mt.getVar("name")
    rep = scriptrunner(port, "http-csrf", ip)

    tags = ["Path", "Form id", "Form action"]
    for scriptrun in rep.hosts[0].services[0].scripts_results:
        output = scriptrun.get("output")
        csrfentity = None
        for line in output.split("\n"):
            if any(x in line for x in tags):
                sline = line.split(":")
                tag = sline[0].lstrip()
                data = ":".join(sline[1::])
                if tag == "Path":
                    csrfentity = mt.addEntity("msploitego.CSFR", data)
                    csrfentity.setValue(data)
                elif tag == "Form id":
                    csrfentity.addAdditionalFields("formid", "Form ID", True, data)
                elif tag == "Form action":
                    csrfentity.addAdditionalFields("formaction", "Form Action", True, data)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['httpenum.py',
#  'http/80:249',
#  'properties.metasploitservice=http/80:249#info=Microsoft IIS httpd 10.0#name=http#proto=tcp#hostid=249#service.name=80/Apache 9#port=80#banner=Apache 9#properties.service= #ip=10.10.10.63#fromfile=/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/msploitdb20180501.xml#state=open']
# dotransform(args)

# {'output': "\n  /css/: Potentially interesting directory w/ listing on 'apache/2.4.25 (ubuntu)'\n  /images/: Potentially interesting directory w/ listing on 'apache/2.4.25 (ubuntu)'\n  /js/: Potentially interesting directory w/ listing on 'apache/2.4.25 (ubuntu)'\n  /uploads/: Potentially interesting folder\n", 'elements': {}, 'id': 'http-enum'}