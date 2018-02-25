import sys
from libnmap.parser import NmapParser

from canari.maltego.message import *

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, ozzy Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

nmapfile = sys.argv[1]
rep = NmapParser.parse_fromfile(nmapfile)

for host in rep.hosts:
    if host.is_up():
        print "host " + host.address + " is up"
        for s in host.services:
            if s.state == "open":
                print("    Service: {0}/{1} ({2})".format(s.port,
                                                      s.protocol,
                                                      s.state))
    else:
        print "host " + host.address + " is down"

# def mycallback(nmaptask):
#    nmaptask = nmap_proc.current_task
#    if nmaptask:
#        print("Task {0} ({1}): ETC: {2} DONE: {3}%".format(nmaptask.name,
#                                                           nmaptask.status,
#                                                           nmaptask.etc,
#                                                           nmaptask.progress))

# nmap_proc = NmapProcess(targets=scanip,options="-sV",event_callback=mycallback)
# nmap_proc.run()
# print(nmap_proc.stdout)
# print(nmap_proc.stderr)