#!/usr/bin/env python

from pprint import pprint

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
# nmap -vv -p 139,445 --script=$(ls /usr/share/nmap/scripts/smb-vuln* | cut -d"/" -f6 | tr '\n' ',' | sed 's/.$//') --script-args=unsafe=1

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

    mt.returnOutput()
    mt.addUIMessage("completed!")
dotransform(sys.argv)
# args = ['smbvuln.py',
#  'smb/139:249',
#  'properties.metasploitservice=smb/139:249#info=Microsoft Windows netbios-ssn#name=smb#proto=tcp#hostid=249#service.name=80/Apache 9#port=139#banner=Apache 9#properties.service= #ip=10.10.10.59#state=open#fromfile=/root/data/scan/hthebox/msploitdb20180517.xml']
# dotransform(args)

