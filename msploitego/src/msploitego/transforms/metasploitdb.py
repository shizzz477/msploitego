from pprint import pprint

from common.msploitdb import MetasploitXML
from common.MaltegoTransform import *
import sys

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    entitytags = ["name", "address", "servicecount", "osname", "state", "mac"]
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    fn = mt.getVar("description")
    mdb = MetasploitXML(fn)
    for host in mdb.hosts:
        hostentity = mt.addEntity("maltego.IPv4Address", host.address)
        hostentity.setValue(host.address)
        hostentity.addAdditionalFields("fromfile", "Source File", True, fn)
        tags = host.gettags()
        for etag in entitytags:
            if etag in tags:
                hostentity.addAdditionalFields(etag, etag, True, host.getVal(etag))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['metasploitdb.py',
#  '/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/msploitdb20180501.xml',
#  'description=/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/msploitdb20180501.xml']
# dotransform(args)

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