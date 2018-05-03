#!/usr/bin/env python

__all__ = [
    'Melement',
    'Nelement'
]
class Melement(object):
    def __init__(self, elem):
        if len(list(elem)) > 0:
            for item in elem:
                if item.text and item.text.strip():
                    setattr(self, item.tag, item.text)

    def getgen(self,elem,cls=None):
        for n in elem:
            if cls:
                yield cls(n)
            else:
                yield n

class Nelement(object):
    def __init__(self, elem):
        self._root = elem

    def getgen(self,elem,cls=None):
        for n in elem:
            if cls:
                yield cls(n)
            else:
                yield n