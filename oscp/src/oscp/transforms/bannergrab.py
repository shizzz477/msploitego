#!/usr/bin/env python
import socket
import pprint
from libnmap.parser import NmapParser
from libnmap.process import NmapProcess

from common.MaltegoTransform import *
import sys

from common.entutil import toPort

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

# pprint(me)
oport = toPort(me)
'''''
buffersize = 1024

try:
    tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsocket.connect((oport.source, int(oport.portnumber)))
    tcpsocket.send("")
    me.debug("message sent successfully")
    data = tcpsocket.recv(buffersize)
    tcpsocket.close()
    me.debug(data)
    me.addEntity('maltego.Banner', data)
    # tcpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # tcpsocket.settimeout(3)
    # tcpsocket.bind((tcpip, tcpport))
    # listen for incoming connections
    # tcpsocket.listen(5)
except socket.error, (value, message):
    me.debug("Error ocurred while creating the socket. Error Code: " + str(value) + ", Error Message: " + message)
    sys.exit(1)
'''''
banner = me.getVar("oscp.banner")
ban = ""

if banner is not None:
    bl = banner.split()
    if "product" in bl[0]:
        ban = " ".join(bl[1:])
    else:
        ban = banner
else:
    def mycallback(nmaptask):
        nmaptask = nmap_proc.current_task
        if nmaptask:
            me.debug("Task {0} ({1}): ETC: {2} DONE: {3}%".format(nmaptask.name,
                                                               nmaptask.status,
                                                               nmaptask.etc,
                                                               nmaptask.progress))

    nmap_proc = NmapProcess(targets=oport.source,
                            options="-vvvv -Pn -p " + oport.portnumber + " -sV --script=banner",
                            event_callback=mycallback)
    nmap_proc.run()
    rep = NmapParser.parse(nmap_proc.stdout)
    for _host in rep.hosts:
        for s in _host.services:
            banner = s.banner
            bl = banner.split()
            if "product" in bl[0]:
                ban = " ".join(bl[1:])
            else:
                ban = banner

    # print(nmap_proc.stdout)
    # print(nmap_proc.stderr)
# me.debug(oport.banner)

me.addEntity('maltego.Banner', ban)
me.addUIMessage("completed!")
me.returnOutput()