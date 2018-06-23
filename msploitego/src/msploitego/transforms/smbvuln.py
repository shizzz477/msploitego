from common.MaltegoTransform import *
import sys
from common.nsescriptlib import scriptrunner

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

scripts = "smb-double-pulsar-backdoor,smb-vuln-conficker,smb-vuln-cve-2017-7494,smb-vuln-cve2009-3103,smb-vuln-ms06-025,smb-vuln-ms07-029,smb-vuln-ms08-067,smb-vuln-ms10-054,smb-vuln-ms10-061,smb-vuln-ms17-010,smb-vuln-regsvc-dos,smb2-vuln-uptime"

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(sys.argv))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    rep = scriptrunner(port, scripts, ip, scriptargs="unsafe=1")
    if rep:
        for scriptrun in rep.hosts[0].scripts_results:
            id = scriptrun.get("id")
            if id and "ERROR" not in scriptrun.get("output"):
                smbvuln = mt.addEntity("msploitego.SambaVulnerability", "{}:{}".format(id,hostid))
                smbvuln.setValue("{}:{}".format(id,hostid))
                smbvuln.addAdditionalFields("description", "Description", False, scriptrun.get("output"))
                smbvuln.addAdditionalFields("IP", "IP Address", False, ip)
                smbvuln.addAdditionalFields("Port", "Port", False, ip)
    else:
        mt.addUIMessage("host is either down or not responding in this port")

    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)

