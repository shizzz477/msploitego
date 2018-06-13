from pprint import pprint

from datetime import datetime
from common.MaltegoTransform import *
from common.postgresdb import MsploitPostgres
import sys
from common.corelib import getFileContents

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
    db = mt.getVar("db")
    user = mt.getVar("user")
    hostid = mt.getVar("id")
    password = mt.getVar("password").replace("\\", "")
    mpost = MsploitPostgres(user, password, db)
    # for loot in mpost.getLootforHost(ip):
    for loot in mpost.getLootforHost(hostid):
        if loot.get("name"):
            lootentity = mt.addEntity("msploitego.MetasploitLoot", "{}:{}".format(loot.get("name"),hostid))
            lootentity.setValue("{}:{}".format(loot.get("name"),hostid))
        else:
            lootentity = mt.addEntity("msploitego.MetasploitLoot", "{}:{}".format(loot.get("ltype"),hostid))
            lootentity.setValue("{}:{}".format(loot.get("ltype"),hostid))
        for k,v in loot.items():
            if isinstance(v,datetime):
                lootentity.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                lootentity.addAdditionalFields(k, k.capitalize(), False, str(v))
        if loot.get("path"):
            filecontents = getFileContents(loot.get("path"))
            if filecontents:
                lootentity.addAdditionalFields("details", "Details", False, "".join(filecontents))
        lootentity.addAdditionalFields("user", "User", False, user)
        lootentity.addAdditionalFields("password", "Password", False, password)
        lootentity.addAdditionalFields("db", "db", False, db)
        lootentity.addAdditionalFields("ip", "IP Address", False, ip)
    mt.returnOutput()

dotransform(sys.argv)
# args = ['postgressloot.py',
#  '10.11.1.5',
#  'ipv4-address=10.11.1.5#ipaddress.internal=false#vuln_count=21#workspace=default#os_family=Windows#purpose=client#os_sp=SP1#created_at=23/1/2018#mac=00:50:56:B8:55:EC#workspace_id=18#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#updated_at=23/1/2018#exploit_attempt_count=7#id=517#state=alive#note_count=84#virtual_host=VMWare#address=10.11.1.5#service_count=8#name=ALICE#os_name=Windows XP#arch=x86#user=msf#db=msf']
# dotransform(args)
