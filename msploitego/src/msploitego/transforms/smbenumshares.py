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
    machinename = mt.getVar("machinename")
    rep = scriptrunner(port, "smb-enum-shares", ip, args="-sU -sS")

    if rep:
        for res in rep.hosts[0].scripts_results:
            output = res.get("output").split("\n")
            regex = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
            bucket = bucketparser(regex,output,method="search")
            for item in bucket:
                warning = item.get("Warning")
                if warning and re.search("denied",warning, re.I):
                    enitiyname = "msploitego.AccessDenied"
                else:
                    enitiyname = "msploitego.SambaShare"
                header = item.get("Header")
                shareentity = mt.addEntity(enitiyname, header)
                shareentity.setValue(header)
                sharename = header.split("\\")[-1].strip().strip(":")
                shareentity.addAdditionalFields("sharename", "Share Name", False, sharename)
                shareentity.addAdditionalFields("sambashare", "Samba Share", False, header)
                shareentity.addAdditionalFields("ip", "IP Address", False, ip)
                shareentity.addAdditionalFields("port", "Port", False, port)
                if machinename:
                    shareentity.addAdditionalFields("machinename", "Machine Name", False, machinename)
                for k,v in item.items():
                    if k == "Header":
                        continue
                    shareentity.addAdditionalFields(k.lower(), k, False, v)
    else:
        mt.addUIMessage("host is either down or not responding in this port")
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
