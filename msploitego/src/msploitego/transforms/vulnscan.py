from pprint import pprint

from libnmap.parser import NmapParser
from libnmap.process import NmapProcess

from common.msploitdb import MetasploitXML
from common.MaltegoTransform import *
import sys
from common.nsescriptlib import scriptrunner

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
#     def mycallback(nmaptask):
#         nmaptask = nmap_proc.current_task
#         if nmaptask:
#             print("Task {0} ({1}): ETC: {2} DONE: {3}%".format(nmaptask.name,
#                                                                nmaptask.status,
#                                                                nmaptask.etc,
#                                                                nmaptask.progress))
#     mt = MaltegoTransform()
#     # mt.debug(pprint(args))
#     mt.parseArguments(args)
#     ip = mt.getVar("address")
#
#     nmap_proc = NmapProcess(targets="10.11.1.8",
#                             options="-sV --script vulscan",
#                             event_callback=mycallback,
#                             safe_mode=False,
#                             fqp="/usr/local/bin/nmap")
#     nmap_proc.run()
#     rep = NmapParser.parse(nmap_proc.stdout)
#     pprint(nmap_proc.stderr)
#
# args = ['enumservices.py',
#  '10.11.1.5',
#  'ipv4-address=10.11.1.5#ipaddress.internal=false#notecount=31#address=10.11.1.5#purpose=server#mac=00:50:56:b8:20:14#osfamily=Linux#servicecount=10#name=10.11.1.5#state=alive#vulncount=31#fromfile=/root/data/report_pack/msploitdb20180524.xml#osname=Linux']
dotransform(sys.argv)


# rep = scriptrunner(None, "vulscan.nse", "10.11.1.5", args="-sV")
# pprint(rep)
    # noteentity = mt.addEntity("maltego.IPv4Address", note.address)
    # noteentity.setValue(note.address)
    # noteentity.addAdditionalFields("fromfile", "Source File", False, fn)
    # tags = note.getTags()
    # for tag in tags:
    #     noteentity.addAdditionalFields(tag.lower(), tag, False, note.getVal(tag))

# mt.returnOutput()
# mt.addUIMessage("completed!")

# dotransform(sys.argv)