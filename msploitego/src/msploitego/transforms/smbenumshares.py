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
__email__ = 'me@me.com'
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

    if rep.hosts[0].status == "up":
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
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['smbenumshares.py',
#  'microsoft-ds/445:517',
#  'properties.samba=microsoft-ds/445:517#ip=10.11.1.5#service.name=microsoft-ds/445:517#macinename=ALICE#banner.text=Microsoft Windows XP microsoft-ds#info=Microsoft Windows XP microsoft-ds#name=microsoft-ds#proto=tcp#created_at=11/3/2018#updated_at=11/3/2018#id=6824#state=open#address=10.11.1.5#host_id=517#port=445#user=msf#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#db=msf']
#
# dotransform(args)
