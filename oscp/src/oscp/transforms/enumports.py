#!/usr/bin/env python
from canari.maltego.entities import IPv4Address
from canari.maltego.utils import debug, progress
from canari.framework import configure #, superuser
from common.nmaputil import getParsedReport
from sploitego.transforms.common.entities import Port

from common.entities import MacAddress

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
    label='OSCP Ports [Enum Ports]',
    description='Enum OSCP host ports',
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
                op.destination = _host.address
                op.protocol = s.protocol
                op.status = s.state
                response += op
            if _host._mac_addr:
                mac = MacAddress(_host._mac_addr)
                mac.source = _host.address
                response += mac
    return response

def onterminate():
    """
    TODO: Write your cleanup logic below or delete the onterminate function and remove it from the __all__ variable
    """
    pass