from pprint import pprint

from libnmap.parser import NmapParser
from libnmap.process import NmapProcess

from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *
from common.corelib import bucketparser

import re

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    pass

    # mt = MaltegoTransform()
    # # mt.debug(pprint(args))
    # mt.parseArguments(args)
    # ip = mt.getValue()
    # options = "-sS -sV -sU -vvvvv -T5 -A"
    # rep = scriptrunner("1-5000", None, ip, args="-sS -sV -T5 -A -Pn")
    # pprint(rep)
    #
    # mt.returnOutput()
    # mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['nmapenumservices.py',
#  '10.11.1.49',
#  'ipv4-address=10.11.1.49#ipaddress.internal=false']
# dotransform(args)
