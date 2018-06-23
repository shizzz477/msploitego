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
__email__ = 'marcgurreri@gmail.com'
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
            vulnentity = mt.addEntity("msploitego.FTPVulnerability", "{}:{}".format(scriptid,hostid))
            vulnentity.setValue("{}:{}".format(scriptid,hostid))
            vulnentity.addAdditionalFields("description", "Description",False,scriptrun.get("output"))
            vulnentity.addAdditionalFields("ip", "IP Address", False, ip)
            vulnentity.addAdditionalFields("port", "Port", False, port)
    else:
        mt.addUIMessage("host is either down or not responding on this port")
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
