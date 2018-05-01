#/usr/bin/env python

import xml.etree.ElementTree as ET
from pprint import pprint

from oscp.src.oscp.transforms.common.corelib import Melement

class MetasploitDb:

    def __init__(self, filename):
        _root = ET.parse(filename).getroot()
        self.hosts = self._getgen(_root.find("hosts"), Mhost)
        self.services = self._getgen(_root.find("services"), Mservice)
        self.websites = self._getgen(_root.find("web_sites"), Mwebsites)
        self.webpages = self._getgen(_root.find("web_pages"), Mwebpages)
        self.webforms = self._getgen(_root.find("web_forms"), Mwebforms)
        self.webvulns = self._getgen(_root.find("web_vulns"), Mwebvulns)
        try:
            _root.remove(_root.find("module_details"))
            _root.remove(_root.find("events"))
        except ValueError:
            print "no module details or events to strip"

    def _getgen(self,elem,cls):
        for e in elem:
            yield cls(e)

class Mhost:
    def __init__(self, elem):
        self.services = None
        self.notes = None
        for item in elem:
            if item.tag == "services":
                self.services = self._getgen(item, Mservice)
            elif item.tag == "notes":
                self.notes = self._getgen(item, Mnote)
            elif item.text and item.text.strip():
                setattr(self, item.tag, item.text)

    def _getgen(self,node,cls):
        for n in node:
            yield cls(n)

    def getOpenServices(self):
        for service in self.services:
            if service.isopen():
                yield service

class Mservice(Melement):
    def __init__(self, elem):
        super(Mservice, self).__init__(elem)

    def isopen(self):
        if self.state.lower() == "open":
            return True
        return False

class Mnote(Melement):
    def __init__(self,elem):
        super(Mnote, self).__init__(elem)

class Mwebsites(Melement):
    def __init__(self,elem):
        super(Mwebsites, self).__init__(elem)

class Mwebpages(Melement):
    def __init__(self,elem):
        super(Mwebpages, self).__init__(elem)

class Mwebforms(Melement):
    def __init__(self,elem):
        super(Mwebforms, self).__init__(elem)

class Mwebvulns(Melement):
    def __init__(self,elem):
        super(Mwebvulns, self).__init__(elem)

mdb = MetasploitDb("msploitdb20180501.xml")
print "class loaded"

hosts = []
for h in mdb.hosts:
    pprint(h)
    for s in h.services:
        pprint(s)
    for n in h.notes:
        pprint(n)
    print "got hosts"

