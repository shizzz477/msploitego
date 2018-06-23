import re
from pprint import pprint
from common.MaltegoTransform import *
from common.linuxtaskrunner import bashrunner
from common.corelib import bucketparser

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

checks = [ re.compile("^\[!\]\sTitle:\s",re.I), re.compile("\[[i+!]\]\s"), re.compile("</"), re.compile("\||\"|\>") ]

def sanitizefield(f):
    global checks
    results = []
    if isinstance(f,list):
        for line in f:
            for regsub in checks:
                line = regsub.sub("",line)
            results.append(line)
    else:
        for regsub in checks:
            f = regsub.sub("",f)
        results.append(f)
    return "".join(results).strip()

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")

    bashlog = bashrunner("wpscan --url {}:{} --enumerate p,u --no-banner --no-color".format(ip,port))
    # regp = re.compile("^\[i]\s", re.I)
    results = bucketparser(re.compile("^\[!\]\sTitle:\s",re.I), bashlog)

    for res in results:
        if res.get("Header"):
            header = sanitizefield(res.get("Header"))
            wpent = mt.addEntity("msploitego.WordpressInfo", header)
            wpent.setValue(header)
            for k,v in res.items():
                if not k or not k.strip() or k == "Header":
                    continue
                k = sanitizefield(k)
                v = sanitizefield(v)
                if v and v.strip() and k and k.strip():
                    wpent.addAdditionalFields(k, k.capitalize(), False, v)
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)