from pprint import pprint

from smb.base import NotReadyError

from smb.SMBConnection import SMBConnection
from common.MaltegoTransform import *
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
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    server = mt.getVar("server")
    if not server:
        server = mt.getVar("machinename")
    workgroup = mt.getVar("workgroup")
    path = mt.getVar("path")
    domaindns = mt.getVar("domain_dns")
    sharename = mt.getVar("sharename")

    if not workgroup:
        workgroup = "WORKGROUP"
    # conn = SMBConnection('', '', "localhost", server, domain=workgroup, use_ntlm_v2=True,is_direct_tcp=True)
    conn = SMBConnection('', '', "localhost", server, domain=workgroup, use_ntlm_v2=True)
    conn.connect(ip, int(port))
    regex = re.compile("^\.{1,2}$")
    try:
        files = conn.listPath(sharename, path)
    except NotReadyError:
        accessdenied = mt.addEntity("msploitego.AccessDenied",sharename)
        accessdenied.setValue(sharename)
    else:
        for f in files:
            filename = checkAndConvertToAscii(f.filename)
            if f.isDirectory:
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
            if domaindns:
                sambaentity.addAdditionalFields("domain_dns", "Domain DNS", False, domaindns)
            sambaentity.addAdditionalFields("sharename", "Share Name", False, sharename)
    conn.close()
    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)
