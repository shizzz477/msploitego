from pprint import pprint

# from msploitego.src.msploitego.transforms.common.entities import Host
from canari.maltego.entities import IPv4Address

from msploitego.src.msploitego.transforms.common.msploitdb import MetasploitXML

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

from common.MaltegoTransform import *
import sys

mt = MaltegoTransform()
mt.debug(pprint(sys.argv))
mt.parseArguments(sys.argv)
pprint(mt.debug(mt.value))
pprint(mt.debug(mt.entities))
pprint(mt.debug(mt.values))
fn = mt.getVar("metasploit.session")
pprint(fn)
mdb = MetasploitXML(fn)
for host in mdb.hosts:
    ipv4 = IPv4Address(host.address)
    mt.addUIMessage("found host {}".format(ipv4))
    mt.addEntity("sploitego.IPv4Address", ipv4)


mt.returnOutput()

"""
    # The transform input entity type.
    input_type = File

    def do_transform(self, request, response, config):
        fname = request.entity
        mdb = MetasploitXML(fname.value)
        for h in mdb.hosts:
            response += h.tomaltego()
        return response
"""