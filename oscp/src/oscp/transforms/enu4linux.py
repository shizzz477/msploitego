#!/usr/bin/env python
import pprint

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
# me.debug(ip)

# enum4 = getEnum4(ip)
sinfo = ServerInfo("SERVERNAME")
# sinfo.servername = "SERVERNAME"
# sinfo.serverdescription = "Description"

me.addEntity('maltego.Phrase', "test phrASE")
me.addEntity('oscp.ServerInfo', sinfo)

me.addUIMessage("completed!")
me.returnOutput()

'''''

enum4 = getEnum4("10.11.1.24")
# me.debug(pprint.pprint(enum4))
for k, d in enum4.iteritems():
    #me.debug(k)
    if k is None:
        pass
    if k == "osinfo":
        #me.debug("**Hit osinfo**")
        #me.debug(pprint.pprint(d))
        srvinfo = d['srvinfo']
        sinfo = ServerInfo(srvinfo['servername'])
        sinfo.servername = srvinfo['servername']
        sinfo.serverdescription = srvinfo['description']
        me.addEntity('oscp.ServerInfo', sinfo)

me.addUIMessage("completed!")
me.returnOutput()

{'srvinfo': {'description': 'Wk Sv PrQ Unx NT SNT payday server (Samba, Ubuntu)',
             'os': 'version :4.9',
             'platform_id': ':500',
             'server': 'type :0x809a03',
             'servername': 'PAYDAY'}}
    if k == "nbtstat":
        nb = Nbtstat(d['WorkstationService'])
        for key, value in d.iteritems():
            setattr(nb, key, value)
        me.addEntity('oscp.Nbtstat', nb)
    if k == "shares":
        pass

'''''