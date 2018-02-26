import sys
from libnmap.parser import NmapParser

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, ozzy Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def addHosts(host, response):
    for host in report.hosts:
        if host.is_up():
            print "host " + host.address + " is up"
            addPorts(host)
        else:
            pass

def addPorts(host):
    for s in host.services:
        if s.state == "open":
            print("  Service: {0}/{1} ({2})".format(s.port,s.protocol,s.state))

nmapfile = sys.argv[1]
rep = NmapParser.parse_fromfile(nmapfile)
addHosts(rep)

