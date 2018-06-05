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
    db = mt.getValue()
    user = mt.getVar("user")
    password = mt.getVar("password").replace("\\","")
    mpost = MsploitPostgres(user, password, db)
    for host in mpost.getAllHosts():
        hostentity = mt.addEntity("maltego.IPv4Address", host.get("address"))
        hostentity.setValue(host.get("address"))
        for k,v in host.items():
            if isinstance(v,datetime):
                hostentity.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                hostentity.addAdditionalFields(k, k.capitalize(), False, str(v))
        hostentity.addAdditionalFields("user", "User", False, user)
        hostentity.addAdditionalFields("password", "Password", False, password)
        hostentity.addAdditionalFields("db", "db", False, db)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['postgreshosts.py',
#  'msf',
#  'properties.postgresqldb=msf#user=msf#password==']
#
# dotransform(args)