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
    mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    path = mt.getVar("uri")
    namelink = mt.getVar("namelink")

    # urlent = mt.addEntity("msploitego.SiteURL", namelink)
    # urlent.setValue(namelink)
    # urlent.addAdditionalFields("ip", "IP Address", False, ip)
    # urlent.addAdditionalFields("port", "Port", False, port)
    mt.returnOutput()
    mt.addUIMessage("completed!")

# dotransform(sys.argv)
args = ['toHashFile.py',
 'ALICE_hashes.txt',
 'properties.lootfile=ALICE_hashes.txt#details=Administrator:500:aad3b435b51404eeaad3b435b51404ee:a8c8b7a37513b7eb9308952b814b522b:::\nHelpAssistant:1000:05fa67eaec4d789ec4bd52f48e5a6b28:2733cdb0d8a1fec3f976f3b8ad1deeef:::\nSUPPORT_388945a0:1002:aad3b435b51404eeaad3b435b51404ee:0f7a50dd4b95cec4c1dea566f820f4e7:::\nalice:1004:aad3b435b51404eeaad3b435b51404ee:b74242f37e47371aff835a6ebcac4ffe:::\n#ip=10.11.1.5']

dotransform(args)
