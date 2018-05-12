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
    entitytags = ["hostid","info", "name", "port", "proto", "state"]
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    fn = mt.getVar("fromfile")
    ip = mt.getVar("address")
    for service in MetasploitXML(fn).gethost(ip).services:
        entityname = "msploitego.MetasploitService"
        if service.state.lower() in ["filtered", "closed"]:
            entityname = "msploitego.ClosedPort"
        hostservice = mt.addEntity(entityname, "{}/{}:{}".format(service.name,service.port,service.hostid))
        hostservice.setValue = "{}/{}:{}".format(service.name,service.port,service.hostid)
        hostservice.addAdditionalFields("ip","IP Address",False,ip)
        if service.name.lower() in ["http","www","https"]:
            hostservice.addAdditionalFields("niktofile", "Nikto File", False, '')
        hostservice.addAdditionalFields("fromfile", "Source File", False, fn)
        for etag in entitytags:
            if etag in service.getTags():
                val = service.getVal(etag)
                hostservice.addAdditionalFields(etag, etag, False, val)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['enumservices.py',
#  '10.10.10.75',
#  'ipv4-address=10.10.10.75#ipaddress.internal=false#fromfile=/root/data/scan/hthebox/msploitdb-20180508.xml#name=TALLY#address=10.10.10.75#servicecount=48#osname=Windows 2016#state=alive#vulncount=0#purpose=server#osflavor=Standard#osfamily=Windows#notecount=23']
# dotransform(args)
