#!/usr/bin/env python

from common.MaltegoTransform import *
import sys

from common.enum4parse import getEnum4
from common.entities import ServerInfo, Nbtstat

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, Oscp Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

me = MaltegoTransform()
me.parseArguments(sys.argv)

ip = me.getVar('ip.source')

enum4 = getEnum4(ip)
for k, d in enum4.iteritems():
    if k == "osinfo":
        srvinfo = d['srvinfo']
        sinfo = ServerInfo(srvinfo['servername'])
        sinfo.servername = srvinfo['servername']
        sinfo.serverdescription = srvinfo['description']
        me.addEntity('oscp.ServerInfo', sinfo)
    if k == "nbtstat":
        nb = Nbtstat(d['WorkstationService'])
        for key, value in d.iteritems():
            setattr(nb, key, value)
        me.addEntity('oscp.Nbtstat', nb)
    if k == "shares":
        pass
