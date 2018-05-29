from pprint import pprint

from common.msploitdb import MetasploitXML
from common.MaltegoTransform import *
import sys

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    pass
    # mt = MaltegoTransform()
    # # mt.debug(pprint(args))
    # mt.parseArguments(args)
    # fn = mt.getVar("fromfile")
    # ip = mt.getVar("address")
    # notetypes = ["pipes founded"]
    # for note in MetasploitXML(fn).gethost(ip).notes:
    #     if note.ntype.lower() in notetypes:
    #         pprint(note)
    #     # noteentity = mt.addEntity("maltego.IPv4Address", note.address)
    #     # noteentity.setValue(note.address)
    #     # noteentity.addAdditionalFields("fromfile", "Source File", False, fn)
    #     # tags = note.getTags()
    #     # for tag in tags:
    #     #     noteentity.addAdditionalFields(tag.lower(), tag, False, note.getVal(tag))
    # mt.returnOutput()
    # mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['enumservices.py',
#  '10.11.1.8',
#  'ipv4-address=10.11.1.8#ipaddress.internal=false#notecount=31#address=10.11.1.8#purpose=server#mac=00:50:56:b8:20:14#osfamily=Linux#servicecount=10#name=10.11.1.8#state=alive#vulncount=31#fromfile=/root/data/report_pack/msploitdb20180524.xml#osname=Linux']
# dotransform(args)
