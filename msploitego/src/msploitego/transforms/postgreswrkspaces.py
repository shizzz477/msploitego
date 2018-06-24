from pprint import pprint

from common.MaltegoTransform import *
from common.postgresdb import MsploitPostgres
from common.corelib import inheritvalues
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
    db = mt.getValue()
    user = mt.getVar("user")
    password = mt.getVar("password").replace("\\","")
    mpost = MsploitPostgres(user, password, db)
    for workspace in mpost.getWorkspaces():
        wsentity = mt.addEntity("msploitego.MetasploitWorkspace", workspace.get("name"))
        wsentity.setValue(workspace.get("name"))
        wsentity.addAdditionalFields("workspaceid", "Workspace Id", False, str(workspace.get("id")))
        wsentity.addAdditionalFields("db", "Database", False, db)
        inheritvalues(wsentity, mt.values)
    mt.returnOutput()
    
dotransform(sys.argv)
# dotransform(args)