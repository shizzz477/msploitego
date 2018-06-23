#!/usr/bin/env python

from libnmap.parser import NmapParser
from libnmap.process import NmapProcess
from pprint import pprint

from corelib import static_var

import sys

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, Metasploitego Project'
__credits__ = []
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

@static_var("TCP_SYN", "-sS")

class Nmaprunner(object):
    def __init__(self, ip, port, callback, options=None,safemode=False):
        if options:
            options = "-vvvvv "+ options
        else:
            options = "-vvvvv"
        # self.options = "-vv {} -p {} {}".format(self.scantype, port, ip)
        self.ip = ip
        self.port = port
        self.callback = callback
        self.nmap_proc = NmapProcess(targets=self.ip,
                                    options=options,
                                    event_callback=self.callback,
                                     safe_mode=safemode)

    def runnmap(self):
        self.nmap_proc.run()
        return NmapParser.parse(self.nmap_proc.stdout)

    def getproc(self):
        return self.nmap_proc

if __name__ == "__main__":
    def mycallback(nmaptask):
        if nmaptask:
            print "Task {0} ({1}): ETC: {2} DONE: {3}%".format(nmaptask.name,nmaptask.status,nmaptask.etc,nmaptask.progress)

    nrunner = Nmaprunner("10.10.10.74", "445", mycallback)
    nrunner.runnmap()
    pprint(nrunner)