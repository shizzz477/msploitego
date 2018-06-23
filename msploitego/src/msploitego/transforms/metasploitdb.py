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
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

def dotransform(args):
    entitytags = ["name", "address", "servicecount", "osname", "state", "mac","vulncount","purpose", "osflavor",
                  "osfamily", "notecount"]
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    fn = mt.getVar("description")
    mdb = MetasploitXML(fn)
    for host in mdb.hosts:
        hostentity = mt.addEntity("maltego.IPv4Address", host.address)
        hostentity.setValue(host.address)
        hostentity.addAdditionalFields("fromfile", "Source File", False, fn)
        tags = host.getTags()
        for etag in entitytags:
            if etag in tags:
                hostentity.addAdditionalFields(etag, etag, False, host.getVal(etag))
    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)
