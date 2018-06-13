from pprint import pprint
from datetime import datetime
from common.MaltegoTransform import *
from common.postgresdb import MsploitPostgres
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
    ip = mt.getValue()
    hostid = mt.getVar("id")
    db = mt.getVar("db")
    user = mt.getVar("user")
    workspace = mt.getVar("workspace")
    password = mt.getVar("password").replace("\\", "")
    arch = mt.getVar("arch")
    osfamily = mt.getVar("os_family")
    mpost = MsploitPostgres(user, password, db)
    for vuln in mpost.getVulnsForHost(hostid):
        vulnentity = mt.addEntity("maltego.Vulnerability", "{}:{}".format(vuln.get("vulnname"),hostid))
        vulnentity.setValue("{}:{}".format(vuln.get("vulnname"),hostid))
        vulnentity.addAdditionalFields("ip", "IP Address", True, ip)
        vulnentity.addAdditionalFields("user", "User", False, user)
        vulnentity.addAdditionalFields("password", "Password", False, password)
        vulnentity.addAdditionalFields("db", "db", False, db)
        if arch:
            vulnentity.addAdditionalFields("arch", "Arch", False, arch)
        vulnentity.addAdditionalFields("workspace", "Workspace", False, workspace)
        vulnentity.addAdditionalFields("osfamily", "OS", False, osfamily)
        for k,v in vuln.items():
            if isinstance(v,datetime):
                vulnentity.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                vulnentity.addAdditionalFields(k, k.capitalize(), False, str(v))
    mt.returnOutput()

dotransform(sys.argv)
# args = ['postgresvulns.py',
#  '10.11.1.5',
#  'ipv4-address=10.11.1.5#ipaddress.internal=false#vuln_count=21#workspace=default#os_family=Windows#purpose=client#os_sp=SP1#created_at=23/1/2018#mac=00:50:56:B8:55:EC#workspace_id=18#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#updated_at=23/1/2018#exploit_attempt_count=7#id=517#state=alive#note_count=84#virtual_host=VMWare#address=10.11.1.5#service_count=8#name=ALICE#os_name=Windows XP#arch=x86#user=msf#db=msf']
# dotransform(args)