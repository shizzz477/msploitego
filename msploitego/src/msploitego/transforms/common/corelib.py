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
    'static_var',
    'bucketparser'
]

def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

def _nextheader(j,d,r):
    while j < len(d) and r.match(d[j]) is None:
        j += 1
    return j-1

def bucketparser(regex,data,sep=":"):
    i = 0
    bucket = []
    while i < len(data):
        if regex.match(data[i]):
            nextindex = _nextheader(i+1,data,regex)
            item = {"Header":data[i].lstrip()}
            details = []
            i += 1
            while i <= nextindex and i < len(data):
                q = data[i].split(sep)
                if len(q) > 1:
                    item.update({q[0].lstrip().capitalize():q[1].lstrip()})
                else:
                    details.append(q)
                i += 1
            if details:
                item['Details'] = details
            bucket.append(item)
        else:
            i += 1
    return bucket

class XMLElement(object):
    def __init__(self, elem, classmapping=None):
        self._dict = {}
        self._mapping = classmapping
        if len(elem) > 0:
            for item in elem:
                self._setprop(item.tag, item)
        else:
            self._setprop(elem.tag, elem)

    def __iter__(self):
        for x,y in self._dict.items():
            yield [x,y]

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

    def containsTag(self,tag):
        return tag in self.getTags()

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
