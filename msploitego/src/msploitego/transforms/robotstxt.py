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
    global nmap_proc
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    rep = scriptrunner(port, "http-robots.txt", ip)

    if rep.hosts[0].status == "up":
        for scriptrun in rep.hosts[0].services[0].scripts_results:
            output = scriptrun.get("output")
            for line in output.split("\n"):
                if line.lstrip()[0] == "/":
                    for d in line.lstrip().strip().split():
                        webdirentity = mt.addEntity("maltego.WebDir", d)
                        webdirentity.setValue(d)
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['httpenum.py',
#  'http/80:249',
#  'properties.metasploitservice=http/80:249#info=Microsoft IIS httpd 10.0#name=http#proto=tcp#hostid=249#service.name=80/Apache 9#port=80#banner=Apache 9#properties.service= #ip=10.10.10.88#fromfile=/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/msploitdb20180501.xml#state=open']
# dotransform(args)
