#!/usr/bin/env python

__all__ = [
    'Melement',
    'Nelement',
    'static_var'
]

def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

class SimpleElement(object):
    def __init__(self):
        self._dict = {}

        def getgen(self, elem, cls=None):
            for n in elem:
                if cls:
                    yield cls(n)
                else:
                    yield n

        def getVal(self, tag):
            return self._dict.get(tag)

        def getTags(self):
            return self._dict.keys()

class SingleElement(SimpleElement):
    def __init__(self, elem):
        super(SingleElement, self).__init__()
        cleantag = elem.tag.replace('-', '')
        setattr(self, cleantag, elem.text)
        self._dict.update({cleantag: elem.text})

class Melement(object):
    def __init__(self, elem):
        # if len(list(elem)) > 0:
        self._dict = {}
        for item in elem:
            cleantag = item.tag.replace('-', '')
            if item.text and item.text.strip():
                setattr(self, cleantag, item.text)
                self._dict.update({cleantag:item.text})

    def getgen(self,elem,cls=None):
        for n in elem:
            if cls:
                yield cls(n)
            else:
                yield n

    def getVal(self,tag):
        return self._dict.get(tag)

    def getTags(self):
        return self._dict.keys()

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