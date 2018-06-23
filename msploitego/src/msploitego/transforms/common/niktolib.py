#!/usr/bin/env python

import xml.etree.ElementTree as ET

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, Metasploitego Project'
__credits__ = []
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

class NiktoReport(object):
    def __init__(self, fn):
        self._root = ET.parse(fn).getroot()
        self.details = None
        for child in self._root:
            self.details = self._gendetails(child)

    def _gendetails(self,elem):
        for child in elem:
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
                text = prop.text
                if isinstance(prop.text, unicode):
                    text = prop.text.encode("ascii","replace")
                setattr(self, prop.tag, text)
                self._dict.update({prop.tag:text})

    def get(self,tag):
        return self._dict.get(tag)
