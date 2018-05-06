#!/usr/bin/env python

__all__ = [
    'Melement',
    'Nelement'
]
class Melement(object):
    def __init__(self, elem):
        if len(list(elem)) > 0:
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
        self._root = elem

    def getgen(self,elem,cls=None):
        for n in elem:
            if cls:
                yield cls(n)
            else:
                yield n