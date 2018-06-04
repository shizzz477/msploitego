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

def setentity(m,p):
    if p.get("code") and p.code == "404":
        return None
    if p.path == "/":
        entityname = "maltego.Website"
    else:
        entityname = "msploitego.SiteURL"
    pageentity = m.addEntity(entityname, "http://{}:{}{}".format(p.host, p.port, p.path))
    pageentity.setValue("http://{}:{}{}".format(p.host, p.port, p.path))
    pageentity.addAdditionalFields("ip", "IP Address", True, p.host)
    pageentity.addAdditionalFields("properties.siteurl", "Site URL", True,
                                   "http://{}:{}{}".format(p.host, p.port, p.path))
    for k, v in p:
        if v and v.strip():
            pageentity.addAdditionalFields(k, k.capitalize(), True, v)

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    fn = mt.getVar("fromfile")
    ip = mt.getVar("address")
    host = MetasploitXML(fn).gethost(ip)
    for page in host.webpages:
        setentity(mt,page)
    for form in host.webforms:
        setentity(mt,form)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['enumservices.py',
#  '10.11.1.115',
#  'ipv4-address=10.11.1.115#ipaddress.internal=false#notecount=6#address=10.11.1.115#purpose=server#mac=00:50:56:b8:f0:4a#osfamily=Windows#servicecount=10#name=BETHANY2#state=alive#vulncount=0#fromfile=/root/data/report_pack/msploitdb20180601.xml#osname=Windows 2012 R2']
# dotransform(args)

