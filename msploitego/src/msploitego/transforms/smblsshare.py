from pprint import pprint
from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *

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

    scriptarg = "share={}".format(mt.getVar("sharename"))
    rep = scriptrunner(port, "smb-ls", ip, scriptargs=scriptarg)
    if rep.hosts[0].status == "up":
        for res in rep.hosts[0].scripts_results:
            output = res.get("output")
            # dirlist = [x for x in output.split("\n") if x.strip()]
            d2 = [ [ y.split()[0],y.split()[-1] ] for y in [x for x in output.split("\n") if x.strip()]]
            # dirlist = [ [y.split()[0],y.split()[-1]] for y in [x for x in output.split("\n")] ]
            for line in d2:
                if re.match("^\<DIR\>", line[0]) and not re.match("^\.{1,2}", line[1]):
                    entityname = "msploitego.SambaShare"
                elif re.match("^[\d]+", line[0]):
                    entityname = "msploitego.SambaFile"
                else:
                    continue
                childentity = mt.addEntity(entityname, line[1])
                childentity.setValue(line[1])
                childentity.addAdditionalFields("sharename", "Share Name", False, mt.getVar("sharename"))
                childentity.addAdditionalFields("ip", "IP Address", False, ip)
                childentity.addAdditionalFields("port", "Port", False, port)
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['smblsshare.py',
#  '\\\\10.11.1.31\\wwwroot: ',
#  'directory.name=\\\\\\\\10.11.1.31\\\\wwwroot: #sharename=wwwroot#sambashare=\\\\\\\\10.11.1.31\\\\wwwroot: #ip=10.11.1.31#port=445#type=STYPE_DISKTREE#current user access=READ#anonymous access=<none>']
# dotransform(args)
