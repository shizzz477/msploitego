import tempfile
from pprint import pprint
from smb.SMBConnection import SMBConnection, OperationFailure
from common.MaltegoTransform import *

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
    workgroup = mt.getVar("workgroup")
    path = mt.getVar("path")
    sambafile = mt.getVar("properties.sambafile")
    sharename = mt.getVar("sharename")
    conn = SMBConnection('', '', "localhost", server, domain=workgroup, use_ntlm_v2=True,is_direct_tcp=True)
    conn.connect(ip, int(port))
    file_obj = tempfile.NamedTemporaryFile()
    try:
        file_attributes, filesize = conn.retrieveFile(sharename, path, file_obj)
    except OperationFailure:
        pass
    else:
        if int(filesize) > 0:
            file_obj.file.seek(0)
            filecontents = mt.addEntity("msploitego.FileContents", sambafile)
            filecontents.setValue(sambafile)
            filecontents.addAdditionalFields("filecontents", "File Contents", False, " ".join(file_obj.file.readlines()))
            filecontents.addAdditionalFields("ip", "IP Address", False, ip)
            filecontents.addAdditionalFields("port", "Port", False, port)
            filecontents.addAdditionalFields("server", "Server", False, server)
            filecontents.addAdditionalFields("workgroup", "Workgroup", False, workgroup)
            filecontents.addAdditionalFields("sharename", "Share Name", False, sharename)
            filecontents.addAdditionalFields("path", "Path", False, path)
            filecontents.addAdditionalFields("hostid", "Hostid", False, hostid)

    conn.close()
    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)
