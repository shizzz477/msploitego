from pprint import pprint

from common.MaltegoTransform import *

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")

    website = mt.addEntity("maltego.Website", "http://{}:{}".format(ip,port))
    website.setValue("http://{}:{}".format(ip,port))
    website.addAdditionalFields("url", "Site URL", False, "http://{}:{}".format(ip,port))
    website.addAdditionalFields("ip", "IP Address", False, ip)
    website.addAdditionalFields("port", "Port", False, port)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['towebsite.py',
#  'possible_wls/80:545',
#  'properties.metasploitservice=possible_wls/80:545#info=Apache/2.2.4 (Ubuntu) PHP/5.2.3-1ubuntu6 ( Powered by PHP/5.2.3-1ubuntu6 )#name=possible_wls#proto=tcp#hostid=545#service.name=possible_wls#port=80#banner=Apache/2.2.4 (Ubuntu) PHP/5.2.3-1ubuntu6 ( Powered by PHP/5.2.3-1ubuntu6 )#properties.service= #ip=10.11.1.24#niktofile=/root/data/oscp_prep/scan_pack/nikto/10.11.1.24-80.xml#state=open#fromfile=/root/data/report_pack/msploitdb20180524.xml']
#
# dotransform(args)
