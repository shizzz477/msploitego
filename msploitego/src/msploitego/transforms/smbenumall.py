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
    mt.debug(pprint(args))
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
    conn = SMBConnection('admin', 'admin', "localhost", server, domain=workgroup, use_ntlm_v2=True,
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

# dotransform(sys.argv)
args = ['smbenumall.py',
 'OBSERVER:THINC',
 'properties.samba=OBSERVER:THINC#date=2013-12-27T23:37:02-08:00#lanmanager=Windows 7 Professional 6.1#server=OBSERVER#workgroup=THINC#account_used=guest#os=Windows 7 Professional 7601 Service Pack 1#service.name=microsoft-ds/445:510#fqdn=observer.thinc.local#ip=10.11.1.218#hostid=510#challenge_response=supported#banner.text=Windows 7 Professional 7601 Service Pack 1#domain_dns=thinc.local#forest_dns=thinc.local#port=445#properties.service=microsoft-ds/445:510#proto=tcp#name=observer.thinc.local#cpe=cpe:/o:microsoft:windows_7::sp1:professional#authentication_level=user#info=Windows 7 Professional 7601 Service Pack 1#message_signing=disabled']

dotransform(args)
