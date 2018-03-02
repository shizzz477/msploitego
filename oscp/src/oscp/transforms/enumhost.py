#!/usr/bin/env python
import pprint
from common.MaltegoTransform import *
import sys
from canari.maltego.entities import IPv4Address, Phrase
from canari.maltego.utils import debug, progress
from canari.framework import configure
from common.nmaputil import getParsedReport, doSmbVuln, getHost

from common.entities import MacAddress, Fingerprint, Port, OHost
from common.coreutil import sanitize

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, Oscp Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

__all__ = [
    'dotransform',
    'onterminate' # comment out this line if you don't need this function.
]

"""
TODO: set the appropriate configuration parameters for your transform.
TODO: Uncomment the line below if the transform needs to run as super-user
"""
#@superuser
@configure(
    label='OSCP Enum [Enum Host]',
    description='Enum OSCP host Info',
    uuids=[ 'oscp.IPv4AddressToPorts_fromNmap' ],
    inputs=[ ( 'oscp', OHost ) ],
    debug=True
)
def dotransform(request, response, config):
    """
    enum OSCP host information
    """
    # me = MaltegoTransform()
    # me.parseArguments(sys.argv)
    ip = request.value
    # debug(ip)
    # _host = getHost(ip)
    # debug(pprint.pprint(_host))
    parsedreport = getParsedReport("/mnt/64G/proj/oscp-maltego/nmapnoping.xml")
    for _host in parsedreport.hosts:
        if _host.address == ip:
            '''''
            scripts = _host.scripts_results
            for res in scripts:
                if res.get('id') == "nbstat":
                    #debug("handling nbstat script result: " + pprint.pprint(res))
                    pass
                elif res.get('id') == "smb2-time":
                    #debug(("handling smb2-time script result: " + pprint.pprint(res)))
                    pass
                elif res.get('id') == "p2p-conficker":
                    #debug(("handling p2p-conficker script result: " + pprint.pprint(res)))
                    pass
                elif res.get('id') == "p2p-conficker":
                    #debug(("handling p2p-conficker script result: " + pprint.pprint(res)))
                    pass
                elif res.get('id') == "smb-os-discovery":
                    #debug(("handling smb-os-discovery script result: " + pprint.pprint(res)))
                    pass
                elif res.get('id') == "smb-security-mode":
                    #debug(("handling smb-security-mode script result: " + pprint.pprint(res)))
                    pass
                elif res.get('id') == "smb2-security-mode":
                    #debug(("handling smb2-security-mode script result: " + pprint.pprint(res)))
                    pass
                else:
                    debug(("** NO HANDLER for " + res.get('id')))
                    pass
                '''''
            for s in _host.services:
                # print pprint.pprint(s)
                if s.state == "open":
                    op = Port(s.port)
                    op.portnumber = s.port
                    op.source = _host.address
                    op.protocol = s.protocol
                    op.state = s.state
                    op.servicename = s.service
                    op.banner = s.banner
                    response += op
            for os in _host.os.osmatches:
                fp = Fingerprint(os.name)
                fp.accuracy = str(os.accuracy)
                fp.osname = os.name
                # debug(("processed figerprint: " + pprint.pprint(fp)))
                # me.addEntity("oscp.Fingerprint", fp)
                response += fp
    return response

def onterminate():
    """
    Write your cleanup logic below or delete the onterminate function and remove it from the __all__ variable
    """
    pass

'''''
            for s in _host.services:
                # print pprint.pprint(s)
                if s.state == "open":
                    op = Port(s.port)
                    op.portnumber = s.port
                    op.source = _host.address
                    op.protocol = s.protocol
                    op.state = s.state
                    op.servicename = s.service
                    op.banner = s.banner
                    debug(("processed port: " + pprint.pprint(op)))
                    
for _host in parsedreport.hosts:
    # print "checking host: " + _host.address
    # print type(ip)
    if _host.address == ip:
        for s in _host.services:
            op = Port(s.port)
            # if op.status == "open":
            op.portnumber = s.port
            op.source = _host.address
            op.protocol = s.protocol
            op.state = s.state
            serviced = s._service
            op.servicename = serviced['name']
            # op.product = serviced['product']
            response += op
        if _host._mac_addr:
            mac = MacAddress(_host._mac_addr)
            mac.source = _host.address
            mac.macaddress = _host._mac_addr
            # lab = Label("testLabel", "TESTLABEL")
            response += mac
        for os in _host.os.osmatches:
            accuracy = os.accuracy
            osname = os.name
            fp = Fingerprint(osname)
            fp.accuracy = str(accuracy)
            fp.osname = osname
            response += fp
'''''