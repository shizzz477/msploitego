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
    db = mt.getVar("db")
    workspaceid = mt.getVar("workspaceid")
    user = mt.getVar("user")
    dbpassword = mt.getVar("password").replace("\\","")
    mpost = MsploitPostgres(user, dbpassword, db)
    for cred in mpost.getCredentials(workspaceid):
        if cred.get("privtype") == "Metasploit::Credential::Password":
            entityname = "msploitego.Password"
            password = cred.get("privdata").split(":")[0]
        elif cred.get("privtype") == "Metasploit::Credential::NTLMHash":
            entityname = "msploitego.EncryptedPassword"
            password = cred.get("privdata")
        else:
            entityname = "msploitego.Credentials"
            password = cred.get("privdata")
        username = cred.get("username")
        coreid = cred.get("coreid")
        credentity = mt.addEntity(entityname, "{}:{}".format(username,coreid))
        credentity.setValue("{}:{}".format(username,coreid))
        credentity.addAdditionalFields("password", "Password", False, password)
        for k,v in cred.items():
            if isinstance(v,datetime):
                credentity.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                credentity.addAdditionalFields(k, k.capitalize(), False, str(v))
    mt.returnOutput()


dotransform(sys.argv)
# dotransform(args)