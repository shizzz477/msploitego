#!/usr/bin/env python

import xml.etree.ElementTree as ET

class NiktoReport(object):
    def __init__(self, fn):
        self._root = ET.parse(fn).getroot()
        self.details = None
        for child in self._root:
            self.details = self._gendetails(child)


    def _gendetails(self,elem):
        for child in elem:
            # if "#TEMPL" not in child.description:
            d = Niktodetail(child)
            if d.description:
                yield d

class Niktodetail(object):
    def __init__(self, e):
        self._dict = {}
        self.description = None
        self.uri = None
        self.namelink = None
        self.iplink = None
        for prop in e:
            if "#TEMPL" in prop.text:
                return None
            else:
                setattr(self, prop.tag, prop.text)
                self._dict.update({prop.tag:prop.text})

    def get(self,tag):
        return self._dict.get(tag)

if __name__ == "__main__":
    nr = NiktoReport("/root/proj/oscp-maltego/msploitego/src/msploitego/resources/10.11.1.22-80.xml")
    dets = []
    for d in nr.details:
        dets.append(d)
