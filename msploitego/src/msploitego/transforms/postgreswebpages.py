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
    db = mt.getVar("db")
    user = mt.getVar("user")
    password = mt.getVar("password").replace("\\", "")
    mpost = MsploitPostgres(user, password, db)
    for page in mpost.getwebpagesforhost(ip):
        urlstring = "http"
        if "ssl" in page.get("protoname"):
            urlstring += "s"
        urlstring += "://{}:{}{}".format(ip,page.get("port"),page.get("path"))
        pageent = mt.addEntity("msploitego.WebURL",urlstring)
        pageent.setValue(urlstring)
        for k,v in page.items():
            if isinstance(v,datetime):
                pageent.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                pageent.addAdditionalFields(k, k.capitalize(), False, str(v))
            pageent.addAdditionalFields("ip", "IP Address", False, ip)

    #     if loot.get("name"):
    #         lootentity = mt.addEntity("msploitego.MetasploitLoot", loot.get("name"))
    #         lootentity.setValue(loot.get("name"))
    #     else:
    #         lootentity = mt.addEntity("msploitego.MetasploitLoot", loot.get("ltype"))
    #         lootentity.setValue(loot.get("ltype"))

    #     lootentity.addAdditionalFields("user", "User", False, user)
    #     lootentity.addAdditionalFields("password", "Password", False, password)
    #     lootentity.addAdditionalFields("db", "db", False, db)
    #     lootentity.addAdditionalFields("ip", "IP Address", False, ip)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['postgreswebpages.py',
#  '10.11.1.31',
#  'ipv4-address=10.11.1.31#ipaddress.internal=false#vuln_count=21#address=10.11.1.31#os_family=Windows#purpose=client#service_count=8#os_sp=SP1#created_at=23/1/2018#mac=00:50:56:B8:55:EC#workspace_id=18#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#updated_at=23/1/2018#exploit_attempt_count=7#name=ALICE#os_name=Windows XP#id=517#state=alive#arch=x86#user=msf#note_count=36#db=msf#virtual_host=VMWare']
# dotransform(args)