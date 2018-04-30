#!/usr/bin/env python
import pprint

from canari.maltego.utils import debug, progress
from canari.framework import configure #, superuser

from common.enum4parse import getEnum4
from common.entities import ServerInfo, Nbtstat, OHost

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, Oscp Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

# me = MaltegoTransform()
# me.parseArguments(sys.argv)
@configure(
    label='Enum4Linux2 Scan',
    description='Parses enum4linux scan',
    uuids=[ 'oscp.enum4Linux_scan' ],
    inputs=[ ( 'oscp', OHost ) ],
    debug=True
)
def dotransform(request, response, config):
    #ip = me.getVar('ip.source')
    ip = request.value
    fields = request.fields
    debug(ip)
    debug(fields)
    debug(pprint.pprint(response))
    debug(pprint.pprint(request))

    enum4 = getEnum4(ip)
    for k, d in enum4.iteritems():
        if k == "osinfo":
            srvinfo = d['srvinfo']
            sinfo = ServerInfo(srvinfo['servername'])
            sinfo.servername = srvinfo['servername']
            sinfo.serverdescription = srvinfo['description']
            response += sinfo
            #me.addEntity('oscp.ServerInfo', sinfo)
        '''''
        if k == "nbtstat":
            nb = Nbtstat(d['WorkstationService'])
            for key, value in d.iteritems():
                setattr(nb, key, value)
            me.addEntity('oscp.Nbtstat', nb)
        if k == "shares":
            pass
        '''''
#me.addUIMessage("completed!")
#me.returnOutput()


#dotransform(raw_input().strip())