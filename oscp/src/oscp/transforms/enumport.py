#!/usr/bin/env python
from canari.maltego.entities import Phrase, IPv4Address
from canari.maltego.utils import debug, progress
from canari.framework import configure #, superuser

from common.entities import Port, Service

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
    label='OSCP Port [Enum Port]',
    description='Enumerate OSCP Port',
    uuids=[ 'oscp.EnumPortInfo_fromnmap' ],
    inputs=[ ( 'Oscp', Port ), ( 'maltego', IPv4Address ) ],
    debug=True
)
def dotransform(request, response, config):
    portnumber, ipaddr = request.value
    # f = request.fields
    # ps = Service(f['servicename'])
    # ps.servicename = f['servicename']
    # ps.portnumber = f['portnumber']
    lab = Phrase(str(portnumber) + " : " + ipaddr)
    response += lab
    return response

def onterminate():
    """
    TODO: Write your cleanup logic below or delete the onterminate function and remove it from the __all__ variable
    """
    pass