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
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    sessionid = mt.getVar("sessionid")
    db = mt.getVar("db")
    user = mt.getVar("user")
    password = mt.getVar("password").replace("\\", "")
    mpost = MsploitPostgres(user, password, db)
    for detail in mpost.getSessionDetails(sessionid):
        detailent = mt.addEntity("msploitego.SessionDetail", str(detail.get("id")))
        detailent.setValue(str(detail.get("id")))
        for k,v in detail.items():
            if isinstance(v,datetime):
                detailent.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                detailent.addAdditionalFields(k, k.capitalize(), False, str(v))
        detailent.addAdditionalFields("user", "User", False, user)
        detailent.addAdditionalFields("password", "Password", False, password)
        detailent.addAdditionalFields("db", "db", False, db)
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
