#!/usr/bin/env python
from pprint import pprint
import sys

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

scripts = {"httpenum":"maltego.WedDir"}

# def _supported(n):
#     return n in scripts
#
# def httpenum(d):
#     pass

# def processNse(name, d):
#     name = cleantag(name)
#     if _supported(name):
#         getattr(sys.modules[__name__], name)(d)
#     else:
#         return "{} not supported".format(name)

def cleantag(tag):
    return tag.replace('-', '')

def cleanresults(r):
    results = {}
    for d in r:
        scriptname = d.get("id")
        resultlist = [x for x in [d.get("output").replace("'", "").replace("/", "").lstrip("\n").lstrip(" ").split("\n")][0] if ":" in x]
        result = {}
        for item in resultlist:
            result.update([item.lstrip().split(":")])
        results.update({cleantag(scriptname): result})
    return results
