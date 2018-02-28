#!/usr/bin/env python
from canari.maltego.entities import IPv4Address
from canari.maltego.utils import debug, progress
from canari.framework import configure #, superuser
from common.nmaputil import getParsedReport

from common.entities import MacAddress, Fingerprint, Port

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
    inputs=[ ( 'maltego', IPv4Address ) ],
    debug=True
)
def dotransform(request, response, config):
    """
    enum the ports for OSCP host
    """
    ip = request.value
    parsedreport = getParsedReport("No file")
    for _host in parsedreport.hosts:
        # print "checking host: " + _host.address
        # print type(ip)
        if _host.address == ip:
            for s in _host.services:
                op = Port(s.port)
                #if op.status == "open":
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
                #lab = Label("testLabel", "TESTLABEL")
                response += mac
            for os in _host.os.osmatches:
                accuracy = os.accuracy
                osname = os.name
                fp = Fingerprint(osname)
                fp.accuracy = str(accuracy)
                fp.osname = osname
                response += fp
    return response

def onterminate():
    """
    Write your cleanup logic below or delete the onterminate function and remove it from the __all__ variable
    """
    pass