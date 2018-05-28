from common.MaltegoTransform import *
import sys
from common.nsescriptlib import scriptrunner

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

scripts = "smb-vuln-conficker,smb-vuln-cve-2017-7494,smb-vuln-cve2009-3103,smb-vuln-ms06-025,smb-vuln-ms07-029,smb-vuln-ms08-067,smb-vuln-ms10-054,smb-vuln-ms10-061,smb-vuln-ms17-010,smb-vuln-regsvc-dos,smb2-vuln-uptime"

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(sys.argv))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")

    rep = scriptrunner(port, scripts, ip)
    for scriptrun in rep.hosts[0].scripts_results:
        id = scriptrun.get("id")
        if id:
            smbvuln = mt.addEntity("msploitego.SambaVulnerability", id)
            smbvuln.setValue(id)
            smbvuln.addAdditionalFields("description", "Description", False, scriptrun.get("output"))
            smbvuln.addAdditionalFields("IP", "IP Address", False, ip)
            smbvuln.addAdditionalFields("Port", "Port", False, ip)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['smbvuln.py',
#  'smb/445:22',
#  'properties.metasploitservice=smb/445:22#info=Windows 2008 Standard SP1 (build:6001) (name:HELPDESK) (workgroup:WORKGROUP )#name=smb#proto=tcp#hostid=22#service.name=80/Apache 9#port=445#banner=Apache 9#properties.service= #ip=10.11.1.145#state=open#fromfile=/root/data/report_pack/msploitdb_oscp-20180325.xml']
# dotransform(args)

