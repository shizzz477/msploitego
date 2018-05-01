#!/usr/bin/env python

from libnmap.parser import NmapParser
from pprint import pprint

from oscp.src.oscp.transforms.common.corelib import Nelement

class Nmapreport(object):
    def __init__(self, fn):
        _report = NmapParser.parse_fromfile(fn)
        self.hosts = self._gethostgen(_report.hosts)

    def _gethostgen(self,hosts):
        for h in hosts:
            if h.status.lower() == "up":
                yield Nhost(h)

class Nhost(Nelement):
    def __init__(self,elem):
        super(Nhost, self).__init__(elem)
        self.services = self._getservices()
        self.address = self._root.address
        self.mac = self._root.mac
        self.osfingerprinted = self._root.os_fingerprinted
        self.status = self._root.status
        self.vendor = self._root.vendor
        self.osmatches = self._getosmatches(self._root.os.osmatches)

    def _getosmatches(self, elem):
        for match in elem:
            if match.accuracy >= 90:
                yield match

    def _getservices(self):
        for s in self._root.services:
            if s.state.lower() == "open":
                yield Nservice(s)

class Nservice(Nelement):
    def __init__(self,elem):
        super(Nservice, self).__init__(elem)
        self.state = self._root.state
        self.port = self._root.port
        self.banner = self._root.banner
        self.protocol = self._root.protocol
        self.servicename = self._root.service

nr = Nmapreport("/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/zenmap-oscp-scan.xml")
print "report loaded"

for h in nr.hosts:
    for s in h.services:
        pprint(s)