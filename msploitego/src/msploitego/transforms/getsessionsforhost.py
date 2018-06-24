from pprint import pprint

from datetime import datetime
from common.corelib import inheritvalues
from common.MaltegoTransform import *
from common.postgresdb import MsploitPostgres
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
    ip = mt.getValue()
    hostid = mt.getVar("id")
    db = mt.getVar("db")
    user = mt.getVar("user")
    password = mt.getVar("password").replace("\\", "")
    mpost = MsploitPostgres(user, password, db)
    for session in mpost.getSessionsForHost(hostid):
        sessionentity = mt.addEntity("msploitego.MeterpreterSession", "{}:{}".format(ip,str(session.get("sessionid"))))
        sessionentity.setValue("{}:{}".format(ip,str(session.get("sessionid"))))
        for k,v in session.items():
            if isinstance(v,datetime):
                sessionentity.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                sessionentity.addAdditionalFields(k, k.capitalize(), False, str(v))
        inheritvalues(sessionentity,mt.values)
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)