#!/usr/bin/env python

"""
from canari.maltego.entities import Phrase, IPv4Address
from canari.maltego.utils import debug, progress
from canari.framework import configure #, superuser

from common.entities import Port, Service
"""
from oscp.transforms.common.nmaputil import getService
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

for arg in sys.argv[1:]:
    me.debug(str(arg) + "\n")

oport = toPort(me)

# s = getService(oport.source, int(oport.portnumber))
# if s is not None:
#    me.debug("Service: " + str(s))


"""
thisent = me.addEntity("maltego.Domain","hello " + domain)

thisent.setType("maltego.Domain")
thisent.setValue("Complex." + domain)
thisent.setWeight(200)

thisent.setDisplayInformation("<h3>Heading</h3><p>content here about" + domain + "!</p>");
thisent.addAdditionalFields("variable","Display Value",True,domain)

me.addUIMessage("completed!")
me.returnOutput()



__all__ = [
    'dotransform',
    'onterminate' # comment out this line if you don't need this function.
]

#@superuser
@configure(
    label='OSCP Port [Enum Port]',
    description='Enumerate OSCP Port',
    uuids=[ 'oscp.EnumPortInfo_fromnmap' ],
    inputs=[ ( 'Oscp', Port )],
    debug=True
)
def dotransform(request, response, config):
    portnumber = request.value
    # f = request.fields
    # ps = Service(f['servicename'])
    # ps.servicename = f['servicename']
    # ps.portnumber = f['portnumber']
    lab = Phrase(str(portnumber))
    response += lab
    return response

def onterminate():
    pass
"""