#!/usr/bin/env python
import io

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

__all__ = [
    'XMLElement',
    'Nelement',
    'static_var',
    'bucketparser',
    'checkAndConvertToAscii',
    'getFileContents',
    'inheritvalues'
]

noinheritfields = ["niktofile", "properties.", "created_at","updated_at","datastore"]

def inheritvalues(ent,values):
    for k,v in values.items():
        if v and v.strip() and not any(x in k for x in noinheritfields):
            ent.addAdditionalFields(k, k.capitalize(), False, v)

def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

def _nextheader(j,d,r,m):
    while j < len(d) and _reg(d[j],m,r) is None:
        j += 1
    return j-1

def _reg(st,meth,reg):
    if meth == "match":
        return reg.match(st)
    elif meth == "search":
        return reg.search(st)

def _checkstring(s):
    if isinstance(s,unicode):
        return s.encode('ascii', 'replace')
    return s

def checkAndConvertToAscii(s):
    if isinstance(s,list):
        newlist = []
        for line in s:
            newlist.append(_checkstring(line))
        return newlist
    return _checkstring(s)

def getFileContents(fn):
    contents = []
    with io.open(fn, 'r', encoding="ascii") as f:
        for line in f:
            if "Target path" in line:
                continue
            asciiline = checkAndConvertToAscii(line)
            contents.append(asciiline.replace('\x00',''))
    return contents

def bucketparser(regex,data,sep=":",method="match",ignoreg=None):
    i = 0
    bucket = []
    while i < len(data):
        if _reg(data[i],method,regex):
            nextindex = _nextheader(i+1,data,regex,method)
            item = {"Header":data[i].lstrip()}
            details = []
            i += 1
            while i <= nextindex and i < len(data):
                if ignoreg and ignoreg.search(data[i]):
                    i += 1
                    continue
                q = data[i].lstrip().replace("http://","http//").replace("https://","https//").split(sep, 1)
                if len(q) > 1:
                    item.update({q[0].lstrip().capitalize():q[1].lstrip().rstrip()})
                else:
                    for line in q:
                        if line and line.strip():
                            details.append(line)
                i += 1
            if details:
                item['Details'] = details
            bucket.append(item)
        else:
            i += 1
    return bucket

class XMLElement(object):
    def __init__(self, elem, classmapping=None, ignore=None):
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

    def get(self,tag):
        return self._dict.get(tag)

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
