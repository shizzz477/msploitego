import re
from pprint import pprint
from common.MaltegoTransform import *
import sys

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
    regex = re.compile("\[V\]\s|\[\+\]\s|\[i\]\s", re.I)
    sidex = re.compile("^S-1-", re.I)
    namex = re.compile("^[\w\.]{2,}\\\\+[\w\.]{2,}")
    data = mt.getVar("data").replace("\\\\","\\").split("\n")
    if data:
        for line in data:
            sid = name = typ = ""
            if line.strip() and not regex.search(line):
                details = line.split()
                for d in details:
                    if sidex.match(d):
                        sid = d
                    elif namex.match(d):
                        name = d
                    elif re.search("group|user",d,re.I):
                        typ = d.strip(")")
                if name:
                    if typ.lower() == "group":
                        entityname = "msploitego.SambaGroupInformation"
                    else:
                        entityname = "msploitego.SambaUser"
                    sambauser = mt.addEntity(entityname, name)
                    sambauser.setValue(name)
                    sambauser.addAdditionalFields("sid", "Sid", False, sid)
                    sambauser.addAdditionalFields("type", "Type", False, typ)
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
