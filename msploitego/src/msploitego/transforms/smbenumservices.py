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
    rep = scriptrunner(port, "smb-enum-services", ip)

    if rep.hosts[0].status == "up":
        for res in rep.hosts[0].services[0].scripts_results:
            output = res.get("output").split("\n")
            regex = re.compile("^\s\s[a-zA-Z0-9_.-]+")
            bucket = bucketparser(regex,output)
            for item in bucket:
                userentity = mt.addEntity("maltego.Service", item.get("Header"))
                userentity.setValue(item.get("Header"))
                userentity.addAdditionalFields("displayname", "Service Name", False, item.get("Display_name"))
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['smbenumservices.py',
#  'smb/445:39',
#  'properties.metasploitservice=smb/445:39#info=Windows 2000 SP0 - 4 (language:English) (name:JD)#name=smb#proto=tcp#hostid=39#service.name=smb#port=139#banner=Windows 2000 SP0 - 4 (language:English) (name:JD)#properties.service= #ip=10.11.1.227#state=open#fromfile=/root/data/report_pack/msploitdb_oscp-20180325.xml']
# dotransform(args)
