#/usr/bin/env python

import xml.etree.ElementTree as ET
from pprint import pprint

class MetasploitDb:

    def __init__(self, filename):
        self._root = ET.parse(filename).getroot()

    def gethosts(self):
        for hosts in self._root.findall('hosts'):
            for host in hosts:
                yield host

class Mhost:
    def __init__(self, elem):
        self.services = []
        self.notes = []
        for item in elem:
            if item.tag == "services":
                for service in item:
                    self.services.append(Mservice(service))
            elif item.tag == "notes":
                for note in item:
                    self.notes.append(Mnote(note))
            elif item.text and item.text.strip():
                setattr(self, item.tag, item.text)

    def getOpenServices(self):
        s = []
        for service in self.services:
            if service.isopen():
                s.append(service)
        return s

class Mservice:
    def __init__(self, elem):
        for item in elem:
            if item.text and item.text.strip():
                setattr(self, item.tag, item.text)

    def isopen(self):
        if self.state.lower() == "open":
            return True
        return False

class Mnote:
    def __init__(self,elem):
        for item in elem:
            if item.text:
                setattr(self, item.tag, item.text)

mdb = MetasploitDb("msploitdb20180430.xml")
print "class loaded"

hosts = []
for h in mdb.gethosts():
    mhost = Mhost(h)
    hosts.append(mhost)
    services = mhost.getOpenServices()
    print "got open services"
print "hosts extracted"
