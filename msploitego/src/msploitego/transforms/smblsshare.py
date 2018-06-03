from pprint import pprint

import unicodedata
from smb.SMBConnection import SMBConnection
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
    server = mt.getVar("server")
    workgroup = mt.getVar("workgroup")
    account = mt.getVar("account_used")
    path = mt.getVar("path")
    domaindns = mt.getVar("domain_dns")
    sharename = mt.getVar("sharename")
    conn = SMBConnection('', '', "localhost", server, domain=workgroup, use_ntlm_v2=True,is_direct_tcp=True)
    conn.connect(ip, int(port))
    regex = re.compile("^\.{1,2}$")
    for file in conn.listPath(sharename, path):
        filename = unicodedata.normalize("NFKD", file.filename).encode('ascii', 'ignore')
        if file.isDirectory:
            if not regex.match(filename):
                entityname = "msploitego.SambaShare"
                newpath = "{}/{}".format(path,filename)
            else:
                continue
        else:
            entityname = "msploitego.SambaFile"
            newpath = "{}/{}".format(path, filename)
        sambaentity = mt.addEntity(entityname,"{}/{}{}".format(ip,sharename,newpath))
        sambaentity.setValue("{}/{}{}".format(ip,sharename,newpath))
        sambaentity.addAdditionalFields("ip", "IP Address", False, ip)
        sambaentity.addAdditionalFields("port", "Port", False, port)
        sambaentity.addAdditionalFields("server", "Server", False, server)
        sambaentity.addAdditionalFields("workgroup", "Workgroup", False, workgroup)
        sambaentity.addAdditionalFields("filename", "Filename", False, filename)
        sambaentity.addAdditionalFields("path", "Path", False, newpath)
        sambaentity.addAdditionalFields("hostid", "Hostid", False, hostid)
        sambaentity.addAdditionalFields("domain_dns", "Domain DNS", False, domaindns)
        sambaentity.addAdditionalFields("sharename", "Share Name", False, sharename)
    conn.close()
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['smblsshare.py',
#  '10.11.1.31/wwwroot/_vti_cnf',
#  'directory.name=10.11.1.31/wwwroot/_vti_cnf#ip=10.11.1.31#port=445#server=RALPH#workgroup=THINC#filename=_vti_cnf#path=//_vti_cnf/#hostid=548#domain_dns=ralph#sharename=wwwroot']
# dotransform(args)
