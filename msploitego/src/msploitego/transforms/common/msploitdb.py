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
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

import xml.etree.ElementTree as ET
from pprint import pprint

from corelib import XMLElement

#TODO:make exclusively for MetasploitDB, create derived entity

class MetasploitXML(XMLElement):

    def __init__(self, fn):
        _root = ET.parse(fn).getroot()
        ignore = ["web_sites","web_pages","web_forms"]
        gentags = {"hosts": Mhost, "services": Mservice, "web_vulns": Mwebvuln}
        super(MetasploitXML, self).__init__(list(_root), gentags, ignore)
        self.websites = []
        self.webpages = []
        self.webforms = []
        self.webvulns = []
        for sites in _root.iter("web_sites"):
            for site in list(sites):
                self.websites.append(Mwebsite(site))
        for pages in _root.iter("web_pages"):
            for page in list(pages):
                self.webpages.append(Mwebpage(page))
        for forms in _root.iter("web_forms"):
            for form in list(forms):
                self.webforms.append(Mwebform(form))
        for vulns in _root.iter("web_vulns"):
            for vuln in list(vulns):
                self.webvulns.append(Mwebvuln(vuln))

    def gethost(self,ip):
        for host in self.hosts:
            if host.getVal("address") == ip:
                for form in self.webforms:
                    if form.host == ip:
                        host.addwebform(form)
                for page in self.webpages:
                    if page.host == ip:
                        host.addwebpage(page)
                for site in self.websites:
                    if site.host == ip:
                        host.addwebsite(site)
                return host

class Mhost(XMLElement):
    def __init__(self, elem):
        gentags = {"services": Mservice, "notes": Mnote, "vulns": Mvuln}
        super(Mhost, self).__init__(elem, gentags)
        self.webforms = []
        self.webpages = []
        self.websites = []
        self.webvulns = []

    def __iter__(self):
        for tag, value in self._dict.items():
            yield [tag,value]

    def addwebform(self,wf):
        self.webforms.append(wf)

    def addwebpage(self,wp):
        self.webpages.append(wp)

    def addwebsite(self, ws):
        self.websites.append(ws)

    def addwebvuln(self, wv):
        self.webvulns.append(wv)

    def getOpenServices(self):
        for service in self.services:
            if service.isopen():
                yield service

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


