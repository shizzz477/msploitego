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

    if rep:
        for scriptrun in rep.hosts[0].services[0].scripts_results:
            scriptid = scriptrun.get("id")
            if scriptid.lower() == "ftp-vuln-cve2010-4221":
                scriptid = "cve-2010-4221"
            vulnentity = mt.addEntity("msploitego.FTPVulnerability", scriptid)
            vulnentity.setValue(scriptid)
            vulnentity.addAdditionalFields("description", "Description",False,scriptrun.get("output"))
            vulnentity.addAdditionalFields("ip", "IP Address", False, ip)
            vulnentity.addAdditionalFields("port", "Port", False, port)
    else:
        mt.addUIMessage("host is either down or not responding on this port")
    mt.returnOutput()

# dotransform(sys.argv)
args = ['ftpvulnscan.py',
 'ftp/21:793',
 'service.name=ftp/21:793#port=21#banner=Microsoft ftpd#properties.service= #workspace=space2#ip=10.10.10.59#hostid=793#created_at=30/4/2018#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#updated_at=30/4/2018#proto=tcp#machinename=TALLY#servicename=ftp#state=open#serviceid=7602#user=msf#db=msf#info=Microsoft ftpd#workspaceid=19']
dotransform(args)
