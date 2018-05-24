#!/usr/bin/env python

__all__ = [
    'MetasploitXML',
    'Mhost',
    'Mservice',
    'Mvuln',
    'Mnote',
    'Mwebsite',
    'Mwebvuln',
    'Mvulnref',
    'Mwebpage'
]
__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

import xml.etree.ElementTree as ET
from pprint import pprint

from corelib import XMLElement
from entities import Host

#TODO:make exclusively for MetasploitDB, create derived entity

class MetasploitXML(XMLElement):

    def __init__(self, fn):
        _root = ET.parse(fn).getroot()
        gentags = {"hosts": Mhost, "services": Mservice, "web_sites": Mwebsite, "web_pages": Mwebpage,
                   "web_forms": Mwebform, "web_vulns": Mwebvuln}
        super(MetasploitXML, self).__init__(list(_root), gentags)

    def gethost(self,ip):
        for host in self.hosts:
            if host.getVal("address") == ip:
                return host

class Mhost(XMLElement):
    def __init__(self, elem):
        gentags = {"services": Mservice, "notes": Mnote, "vulns": Mvuln}
        super(Mhost, self).__init__(elem, gentags)

    def __iter__(self):
        for tag, value in self._dict.items():
            yield [tag,value]

    def getOpenServices(self):
        for service in self.services:
            if service.isopen():
                yield service

    def tomaltego(self):
        h = Host()
        h.transform(self)
        return h

class Mservice(XMLElement):
    def __init__(self, elem):
        super(Mservice, self).__init__(elem)

    def isopen(self):
        if self.state.lower() == "open":
            return True
        return False

class Mvuln(XMLElement):
    def __init__(self,elem):
        super(Mvuln, self).__init__(elem, {"refs":Mvulnref})

class Mnote(XMLElement):
    def __init__(self,elem):
        super(Mnote, self).__init__(elem)

class Mvulnref(XMLElement):
    def __init__(self,elem):
        super(Mvulnref, self).__init__(elem)

class Mwebsite(XMLElement):
    def __init__(self,elem):
        super(Mwebsite, self).__init__(elem)

class Mwebpage(XMLElement):
    def __init__(self,elem):
        super(Mwebpage, self).__init__(elem)

class Mwebform(XMLElement):
    def __init__(self,elem):
        super(Mwebform, self).__init__(elem)

class Mwebvuln(XMLElement):
    def __init__(self,elem):
        super(Mwebvuln, self).__init__(elem)

# mdb = MetasploitXML("/root/data/scan/hthebox/msploitdb-20180508.xml")
# print "class loaded"
# for h in mdb.hosts:
#     for s in h.services:
#         pprint(s)
#     for v in h.vulns:
#         pprint(v)
#         if v.refs:
#             for ref in v.refs:
#                 pprint(ref)
#     for n in h.notes:
#         pprint(n)


