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
    excludes = ["Nessus Scan Information"]
    # entitytags = ["hostid", "info", "name","vulnattemptcount"]
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    fn = mt.getVar("fromfile")
    ip = mt.getVar("address")
    host = MetasploitXML(fn).gethost(ip)

    vulncount = int(mt.getVar("vulncount"))
    if vulncount > 0:
        for vuln in host.vulns:
            vulnent = mt.addEntity("maltego.Vulnerability", vuln.name)
            vulnent.setValue(vuln.name)
            vulnent.addAdditionalFields("refs", "References", False, ",".join([x.ref for x in vuln.refs]))
            for tag,val in vuln:
                vulnent.addAdditionalFields(tag, tag.capitalize() , False, val)
                pprint(tag,vuln)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['enumservices.py',
#  '10.10.10.71',
#  'ipv4-address=10.10.10.71#ipaddress.internal=false#fromfile=/root/data/scan/hthebox/msplotdb20180522.xml#name=10.10.10.71#address=10.10.10.71#servicecount=76#osname=Windows 2008 R2#state=alive#vulncount=194#purpose=server#osfamily=Windows#notecount=34']
# dotransform(args)
