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
    creds = mpost.getCredentials()
    for cred in mpost.getCredentials():
        if cred.get("type") == "Metasploit::Credential::Password":
            entityname = "msploitego.Password"
            data = cred.get("data").split(":")[0]
        elif cred.get("type") == "Metasploit::Credential::NTLMHash":
            entityname = "msploitego.EncryptedPassword"
            data = cred.get("data")
        else:
            entityname = "msploitego.Credentials"
            data = cred.get("data")
        hostentity = mt.addEntity(entityname, data)
        hostentity.setValue(data)
        for k,v in cred.items():
            if isinstance(v,datetime):
                hostentity.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                hostentity.addAdditionalFields(k, k.capitalize(), False, str(v))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['postgreshosts.py',
#  'msf',
#  'properties.postgresqldb=msf#user=msf#password=password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=']
# dotransform(args)