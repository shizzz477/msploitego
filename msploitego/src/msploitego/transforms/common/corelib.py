#!/usr/bin/env python

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

__all__ = [
    'XMLElement',
    'Nelement',
    'static_var'
]

def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

class XMLElement(object):
    def __init__(self, elem, classmapping=None):
        self._dict = {}
        self._mapping = classmapping
        if len(elem) > 0:
            for item in elem:
                self._setprop(item.tag, item)
        else:
            self._setprop(elem.tag, elem)

    def _setprop(self,prop,val):
        dictval = None
        prop = self.cleantag(prop)
        if len(val) == 0:
            if val.text and val.text.strip():
                dictval = val.text.strip()
                setattr(self, prop, dictval)
        else:
            if self._mapping and prop in self._mapping:
                cls = self._mapping.get(prop)
                dictval = self.getgen(val, cls)
                setattr(self, prop, dictval)
        if dictval:
            self._dict.update({prop: dictval})

    def setmapping(self, mapping):
        self._mapping = mapping

    @staticmethod
    def getgen(elem, cls=None):
        for n in elem:
            if cls:
                yield cls(n)
            else:
                yield n

    def getVal(self, tag):
        return self._dict.get(tag)

    def getTags(self):
        return self._dict.keys()

    @staticmethod
    def cleantag(tag):
        return tag.replace('-','')

class Nelement(object):
    def __init__(self, elem):
        if elem is not None:
            self._dict = elem.get_dict()
            # for item in elem:
            #     cleantag = item.tag.replace('-', '')
            #     if item.text and item.text.strip():
            #         setattr(self, cleantag, item.text)
            #         self._dict.update({cleantag:item.text})

    def getVal(self,tag):
        return self._dict.get(tag)

    def getTags(self):
        return self._dict.keys()

    def getgen(self,elem,cls=None):
        for n in elem:
            if cls:
                yield cls(n)
            else:
                yield n