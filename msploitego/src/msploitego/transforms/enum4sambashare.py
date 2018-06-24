import re
from pprint import pprint
from common.MaltegoTransform import *
import sys

from common.corelib import bucketparser

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
    cleanse = re.compile("\[\+\]|denied|warning|failed|attempted|attempting|reconnecting", re.I)
    # cleanse = re.compile("\[\+\]|\[v\]")
    data = mt.getVar("data").split("\n")
    # regex = re.compile("^Sharename")
    # results = bucketparser(regex, data, sep=" ")
    res = []
    for line in data:
        if "---" in line or not line or cleanse.search(line):
            continue
        res.append(line)
    pprint(res)
    # if data:
    #     for line in data:
    #         sid = name = typ = ""
    #         if line.strip() and not regex.search(line):
    #             details = line.split()
    #             for d in details:
    #                 if sidex.match(d):
    #                     sid = d
    #                 elif namex.match(d):
    #                     name = d
    #                 elif re.search("group|user",d,re.I):
    #                     typ = d.strip(")")
    #             if name:
    #                 if typ.lower() == "group":
    #                     entityname = "msploitego.SambaGroupInformation"
    #                 else:
    #                     entityname = "msploitego.SambaUser"
    #                 sambauser = mt.addEntity(entityname, name)
    #                 sambauser.setValue(name)
    #                 sambauser.addAdditionalFields("sid", "Sid", False, sid)
    #                 sambauser.addAdditionalFields("type", "Type", False, typ)
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
