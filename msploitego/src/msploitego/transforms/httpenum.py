import shlex
from libnmap.parser import NmapParser
from pprint import pprint
import subprocess
from common.nsescriptlib import cleanresults
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

nmap_proc = None

def mycallback(nmaptask):
    nmaptask = nmap_proc.current_task
    if nmaptask:
        print "Task {0} ({1}): ETC: {2} DONE: {3}%".format(nmaptask.name,
                                                              nmaptask.status,
                                                              nmaptask.etc,
                                                              nmaptask.progress)
def cleanoutput(d):
    return [x for x in [d.get("output").replace("'", "").replace("/", "").lstrip("\n").lstrip(" ").split("\n")][0] if ":" in x]

def dotransform(args):
    global nmap_proc
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    cmd = "nmap -p {} -oX - -vvvvvv --script http-enum {}".format(port,ip)

    nmap_proc = subprocess.Popen(args=shlex.split(cmd),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True,
                                bufsize=0)
    xmloutput = []
    while nmap_proc.poll() is None:
        for streamline in iter(nmap_proc.stdout.readline, ''):
            xmloutput.append(streamline)

    rep = NmapParser.parse(" ".join(xmloutput))
    r = cleanresults(rep.hosts[0].services[0].scripts_results,cleanoutput)

    for scriptname, result in r.items():
        if scriptname == "httpenum":
            for directory, description in result.items():
                webdirentity = mt.addEntity("maltego.WebDir", directory)
                webdirentity.setValue(directory)
                webdirentity.addAdditionalFields("description", "Description", True, description)
    mt.returnOutput()
    mt.addUIMessage("completed!")

# dotransform(sys.argv)
args = ['httpenum.py',
 'http/80:249',
 'properties.metasploitservice=http/80:249#info=Microsoft IIS httpd 10.0#name=http#proto=tcp#hostid=249#service.name=80/Apache 9#port=80#banner=Apache 9#properties.service= #ip=10.10.10.80#fromfile=/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/msploitdb20180501.xml#state=open']
dotransform(args)

# {'output': "\n  /css/: Potentially interesting directory w/ listing on 'apache/2.4.25 (ubuntu)'\n  /images/: Potentially interesting directory w/ listing on 'apache/2.4.25 (ubuntu)'\n  /js/: Potentially interesting directory w/ listing on 'apache/2.4.25 (ubuntu)'\n  /uploads/: Potentially interesting folder\n", 'elements': {}, 'id': 'http-enum'}