from pprint import pprint

from common.nsescriptlib import scriptrunner
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
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    rep = scriptrunner(port, "ftp-vuln-cve2010-4221,ftp-vsftpd-backdoor,ftp-anon,ftp-libopie,ftp-proftpd-backdoor", ip)

    for scriptrun in rep.hosts[0].services[0].scripts_results:
        vulnentity = mt.addEntity("msploitego.FTPVulnerability", "{}:{}".format(scriptrun.get("id"),hostid))
        vulnentity.setValue("{}:{}".format(scriptrun.get("id"),hostid))
        vulnentity.addAdditionalFields("description", "Description",False,scriptrun.get("output"))
        vulnentity.addAdditionalFields("ip", "IP Address", False, ip)
        vulnentity.addAdditionalFields("port", "Port", False, port)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['ftpvulnscan.py',
#  'ftp/21:506',
#  'properties.metasploitservice=ftp/21:506#info=220 Femitter FTP Server ready.\\\\x0d\\\\x0a#name=ftp#proto=tcp#hostid=506#service.name=ftp#port=21#banner=220 Femitter FTP Server ready.\\\\x0d\\\\x0a#properties.service= #ip=10.11.1.125#state=open#fromfile=/root/data/report_pack/msploitdb20180601.xml']
# dotransform(args)
