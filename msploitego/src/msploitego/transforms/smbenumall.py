from pprint import pprint

from common.MaltegoTransform import *
import unicodedata
from smb.SMBConnection import SMBConnection, SMB_FILE_ATTRIBUTE_DIRECTORY
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
    server = mt.getVar("server")
    workgroup = mt.getVar("workgroup")
    account = mt.getVar("account_used")
    path = mt.getVar("sambapath")
    domaindns = mt.getVar("domain_dns")
    if not path:
        path = "/"
    conn = SMBConnection('', '', "localhost", server, domain=workgroup, use_ntlm_v2=True,
                         is_direct_tcp=True)
    conn.connect(ip, int(port))
    shares = conn.listShares()
    regex = re.compile("^\.{1,2}$")
    for share in shares:
        if not share.isSpecial and share.name not in ['NETLOGON', 'SYSVOL']:
            sharename = unicodedata.normalize("NFKD", share.name).encode('ascii', 'ignore')
            for file in conn.listPath(share.name, path):
                filename = unicodedata.normalize("NFKD", file.filename).encode('ascii', 'ignore')
                if file.isDirectory:
                    if not regex.match(filename):
                        entityname = "msploitego.SambaShare"
                        newpath = "{}/{}/".format(path,filename)
                    else:
                        continue
                        # subpath = conn.listPath(share.name, '/{}'.format(filename))
                else:
                    entityname = "msploitego.SambaFile"
                    newpath = "{}/{}".format(path, filename)
                sambaentity = mt.addEntity(entityname,"{}/{}/{}".format(ip,sharename,filename))
                sambaentity.setValue("{}/{}/{}".format(ip,sharename,filename))
                sambaentity.addAdditionalFields("ip", "IP Address", False, ip)
                sambaentity.addAdditionalFields("port", "Port", False, port)
                sambaentity.addAdditionalFields("server", "Server", False, server)
                sambaentity.addAdditionalFields("workgroup", "Workgroup", False, workgroup)
                sambaentity.addAdditionalFields("filename", "Filename", False, filename)
                sambaentity.addAdditionalFields("path", "Path", False, newpath)
                sambaentity.addAdditionalFields("hostid", "Hostid", False, hostid)
                sambaentity.addAdditionalFields("domain_dns", "Domain DNS", False, domaindns)
                sambaentity.addAdditionalFields("sharename", "Share Name", False, sharename)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['smbenumall.py',
#  'RALPH:THINC',
#  'properties.samba=RALPH:THINC#ip=10.11.1.31#port=445#server=RALPH#workgroup=THINC#hostid=548#info=Windows Server 2003 3790 Service Pack 1#name=ralph#banner.text=Windows Server 2003 3790 Service Pack 1#service.name=microsoft-ds/445:548#properties.service=microsoft-ds/445:548#proto=tcp#fqdn=ralph#authentication_level=user#os=Windows Server 2003 3790 Service Pack 1#cpe=cpe:/o:microsoft:windows_server_2003::sp1#message_signing=disabled#domain_dns=ralph#challenge_response=supported#date=2018-06-02T12:23:39-05:00#account_used=guest#lanmanager=Windows Server 2003 5.2']
# dotransform(args)
