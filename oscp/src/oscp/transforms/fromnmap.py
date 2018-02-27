#!/usr/bin/env python
from canari.maltego.entities import Phrase, IPv4Address
from canari.maltego.utils import debug, progress
from canari.framework import configure
from canari.pkgutils import maltego

from common.nmaputil import getParsedReport
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
filepath = "/mnt/64G/proj/oscp-maltego/samplenmap.xml"

@configure(
    label='OSCP Enum Hosts [Enum Hosts]',
    description='enumerate the hosts that have open ports',
    uuids=[ 'TODO oscp.PhrasetoIPv4Addresses_Fromnmap' ],
    inputs=[ ( 'Maltego', Phrase ) ],
    debug=True
)
def dotransform(request, response, config):
    """
    enumerate the hosts that have open ports from an nmap scan file
    """
    # ip = request.value
    parsedreport = getParsedReport(filepath)
    for _host in parsedreport.hosts:
        if _host.is_up():
            ipaddr = IPv4Address(_host.address)
            response += ipaddr
    return response


def onterminate():
    pass