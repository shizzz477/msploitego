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
    rep = scriptrunner(port, "imap-capabilities,imap-ntlm-info", ip)
    if rep.hosts[0].status == "up":
        for scriptrun in rep.hosts[0].services[0].scripts_results:
            infoentity = mt.addEntity("msploitego.RelevantInformation", "{}:{}".format(scriptrun.get("id"),hostid))
            infoentity.setValue("{}:{}".format(scriptrun.get("id"),hostid))
            infoentity.addAdditionalFields("description", "Description",False,scriptrun.get("output"))
            infoentity.addAdditionalFields("ip", "IP Address", False, ip)
            infoentity.addAdditionalFields("port", "Port", False, port)
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['imapscan.py',
# 'imap/143:545',
#  'properties.metasploitservice=imap/143:545#info=Dovecot imapd#name=imap#proto=tcp#hostid=545#service.name=imap#port=143#banner=Dovecot imapd#properties.service= #ip=10.11.1.24#state=open#fromfile=/root/data/report_pack/msploitdb20180601.xml']
# dotransform(args)
