from pprint import pprint
import re
from datetime import datetime
from common.MaltegoTransform import *
from common.postgresdb import MsploitPostgres
import sys
from common.servicefactory import getserviceentity, getosentity

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
    password = mt.getVar("password").replace("\\", "")
    mpost = MsploitPostgres(user, password, db)
    for vuln in mpost.getforHost(ip, "vulns"):
        vulnentity = mt.addEntity("maltego.Vulnerability", "{}:{}".format(vuln.get("name"),hostid))
        vulnentity.setValue("{}:{}".format(vuln.get("name"),hostid))
        vulnentity.addAdditionalFields("ip", "IP Address", True, ip)
        for k,v in vuln.items():
            if isinstance(v,datetime):
                vulnentity.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                vulnentity.addAdditionalFields(k, k.capitalize(), False, str(v))
        vulnentity.addAdditionalFields("user", "User", False, user)
        vulnentity.addAdditionalFields("password", "Password", False, password)
        vulnentity.addAdditionalFields("db", "db", False, db)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['postgresservices.py',
#  '10.11.1.5',
#  'ipv4-address=10.11.1.5#ipaddress.internal=false#updated_at=23/1/2018#vuln_count=21#exploit_attempt_count=7#id=517#state=alive#os_family=Windows#os_name=Windows XP#workspace_id=18#note_count=36#mac=00:50:56:B8:55:EC#service_count=8#purpose=client#address=10.11.1.5#arch=x86#os_sp=SP1#name=ALICE#created_at=23/1/2018#virtual_host=VMWare']
# dotransform(args)