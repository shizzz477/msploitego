#!/usr/bin/env python

__all__ = [
    'MetasploitXML',
    'Mhost',
    'Mservice',
    'Mvuln',
    'Mnote',
    'Mwebsites'
]

import xml.etree.ElementTree as ET
from pprint import pprint

from corelib import Melement, SingleElement
from entities import Host

class MetasploitXML:

    def __init__(self, fn):
        _root = ET.parse(fn).getroot()
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
            pass

    def _getgen(self,elem,cls):
        for e in elem:
            yield cls(e)

    def gethost(self,ip):
        for host in self.hosts:
            if host.getVal("address") == ip:
                return host

class Mhost:
    def __init__(self, elem):
        self.services = []
        self.notes = []
        self.vulns = []
        self._dict = {}
        for item in elem:
            if item.tag == "services":
                self.services = self._getgen(item, Mservice)
            elif item.tag == "notes":
                self.notes = self._getgen(item, Mnote)
            elif item.tag == "vulns":
                self.vulns = self._getgen(item, Mvuln)
            elif item.text and item.text.strip():
                cleantag = item.tag.replace('-','')
                setattr(self, cleantag, item.text)
                self._dict.update({cleantag:item.text})

    def __iter__(self):
        for tag, value in self._dict.items():
            yield [tag,value]

    def _getgen(self,node,cls):
        for n in node:
            yield cls(n)

    def getOpenServices(self):
        for service in self.services:
            if service.isopen():
                yield service

    def gettags(self):
        return self._dict.keys()

    def getVal(self, tag):
        return self._dict.get(tag)

    def tomaltego(self):
        h = Host()
        h.transform(self)
        return h

class Mservice(Melement):
    def __init__(self, elem):
        super(Mservice, self).__init__(elem)

    def isopen(self):
        if self.state.lower() == "open":
            return True
        return False

class Mvuln(object):
    def __init__(self,elem):
        self._dict = {}
        # super(Mvuln, self).__init__(elem)
        self.vulnrefs = []
        for prop in elem:
            if prop.tag == "refs":
                for ref in prop:
                    vr = Mvulnref(ref)
                    self.vulnrefs.append(vr)
                    print "ref"
            if prop.text and prop.text.strip():
                cleantag = prop.tag.replace('-', '')
                setattr(self, cleantag, prop.text.strip())
                self._dict.update({cleantag: prop.text.strip()})

class Mnote(Melement):
    def __init__(self,elem):
        super(Mnote, self).__init__(elem)

class Mvulnref(SingleElement):
    def __init__(self,elem):
        super(Mvulnref, self).__init__(elem)

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

# mdb = MetasploitXML("/root/data/scan/hthebox/msploitdb20180502.xml")
# print "class loaded"
# hosts = []
# for h in mdb.hosts:
#     pprint(h)
# website = mdb.websites.next()
# webpage = mdb.webpages.next()
# webform = mdb.webforms.next()
# vuln = mdb.webvulns.next()

# print "subclasses loaded"
# hosts = []
# for h in mdb.hosts:
#     pprint(h)
#     vulns = [x for x in h.vulns]
#     print "got vulns"
#     for s in h.services:
#         pprint(s)
#     for n in h.notes:
#         pprint(n)
#     print "got hosts"

