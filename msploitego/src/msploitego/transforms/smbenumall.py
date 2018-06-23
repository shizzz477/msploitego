from pprint import pprint

from common.MaltegoTransform import *
from smb.SMBConnection import SMBConnection, SMB_FILE_ATTRIBUTE_DIRECTORY
import re
from common.corelib import checkAndConvertToAscii

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
    mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    server = mt.getVar("server")
    workgroup = mt.getVar("workgroup")
    account = mt.getVar("account_used")
    if not account:
        account = ""
    path = mt.getVar("sambapath")
    domaindns = mt.getVar("domain_dns")
    if not path:
        path = "/"
    conn = SMBConnection(account, '', "localhost", server, domain=workgroup, use_ntlm_v2=True,is_direct_tcp=True)
    try:
        conn.connect(ip, int(port))
    except Exception:
        mt.addException("Could not connect to samba server")
    else:
        shares = conn.listShares()
        regex = re.compile("^\.{1,2}$")
        for share in shares:
            if not share.isSpecial and share.name not in ['NETLOGON', 'SYSVOL']:
                sharename = checkAndConvertToAscii(share.name)
                for f in conn.listPath(share.name, path):
                    filename = checkAndConvertToAscii(f.filename)
                    if f.isDirectory:
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

dotransform(sys.argv)
# dotransform(args)
