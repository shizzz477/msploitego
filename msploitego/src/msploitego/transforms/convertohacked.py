from pprint import pprint

from common.MaltegoTransform import *

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
    module = mt.getValue()

    falsepos = mt.addEntity("msploitego.Hacked", "{}:{}".format(module,ip,port))
    falsepos.setValue("{}:{}".format(module,ip,port))
    falsepos.addAdditionalFields("ip", "IP Address", False, ip)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['convertofalsetrue.py',
#  'auxiliary/scanner/smb/smb_ms17_010',
# 'properties.metasploitmodule=auxiliary/scanner/smb/smb_ms17_010#rank=normal#details=MS17-010 SMB RCE Detection\n#ip=10.11.1.73']
# dotransform(args)
