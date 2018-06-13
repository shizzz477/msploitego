from pprint import pprint
import re
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
        vulnentity.addAdditionalFields("db", "db", False, db)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# dotransform(args)