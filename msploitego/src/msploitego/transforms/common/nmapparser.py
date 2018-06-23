#!/usr/bin/env python

from libnmap.parser import NmapParser
from pprint import pprint

from corelib import Nelement

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, Metasploitego Project'
__credits__ = []
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'


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
        self.services = self._getservices(elem.services)
        self.address = elem.address
        if elem.mac:
            self.mac = elem.mac
        self.osfingerprinted = elem.os_fingerprinted
        self.status = elem.status
        self.vendor = elem.vendor
        self.osmatches = self._getosmatches(elem.os.osmatches)
        if len(elem.scripts_results) > 0:
            self.scriptresults = self.getgen(elem.scripts_results, Nscriptresults)

    def _getosmatches(self, elem):
        for match in elem:
            if match.accuracy >= 90:
                yield match

    def _getservices(self, elem):
        for s in elem:
            if s.state.lower() == "open":
                yield Nservice(s)

class Nservice(Nelement):
    def __init__(self,elem):
        super(Nservice, self).__init__(elem)
        self.state = elem.state
        self.port = elem.port
        self.banner = elem.banner
        self.protocol = elem.protocol
        self.servicename = elem.service

class Nscriptresults(Nelement):
    def __init__(self,elem):
        super(Nscriptresults, self).__init__(elem)
