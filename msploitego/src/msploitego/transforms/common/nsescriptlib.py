#!/usr/bin/env python

import shlex
import subprocess
from libnmap.parser import NmapParser
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

def cleantag(tag):
    return tag.replace('-', '')

def cleanresults(r,func):
    results = {}
    for d in r:
        scriptname = d.get("id")
        resultlist = func(d)
        result = {}
        for item in resultlist:
            result.update([item.lstrip().split(":")])
        results.update({cleantag(scriptname): result})
    return results

def scriptrunner(port,name,ip,args=None,scriptargs=None):
    #TODO: exception handling
    if args:
        cmd = "nmap {} -p {} -oX - -vvvvvv --script {} {}".format(args, port, name, ip)
    else:
        cmd = "nmap -p {} -oX - -vvvvvv --script {} {}".format(port,name,ip)

    if scriptargs:
        cmd += " --script-args {}".format(scriptargs)

    nmap_proc = subprocess.Popen(args=shlex.split(cmd),
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                universal_newlines=True,
                                bufsize=0)
    xmloutput = []
    while nmap_proc.poll() is None:
        for streamline in iter(nmap_proc.stdout.readline, ''):
            xmloutput.append(streamline)
    return NmapParser.parse(" ".join(xmloutput))
