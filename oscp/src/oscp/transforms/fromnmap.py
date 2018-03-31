#!/usr/bin/env python
from canari.maltego.entities import Phrase, IPv4Address
from canari.maltego.utils import debug, progress
from canari.framework import configure
from canari.pkgutils import maltego
from sploitego.transforms.common.entities import NmapReport

from common.nmaputil import getParsedReport
from common.entities import MacAddress, OHost

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
# filepath = "/mnt/64G/proj/oscp-maltego/nmapnoping.xml"

@configure(
    label='OSCP Enum Hosts [Enum Hosts]',
    description='enumerate the hosts that have open ports',
    uuids=[ 'TODO oscp.PhrasetoIPv4Addresses_Fromnmap' ],
    inputs=[ ( 'Sploitego', NmapReport ) ],
    debug=True
)
def dotransform(request, response, config):
    """
    enumerate the hosts that have open ports from an nmap scan file
    """
    filepath = request.value
    debug("filepath: "+filepath)
    parsedreport = getParsedReport(filepath)
    for _host in parsedreport.hosts:
        if _host.is_up():
            h = IPv4Address(_host.ipv4)
            h.source = _host.ipv4
            # h.mac = _host.mac
            # h.vendor = _host.vendor
            response += h
    return response


def onterminate():
    pass