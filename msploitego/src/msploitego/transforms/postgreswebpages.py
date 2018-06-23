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
    ip = mt.getValue()
    db = mt.getVar("db")
    hostid = mt.getVar("id")
    user = mt.getVar("user")
    password = mt.getVar("password").replace("\\", "")
    mpost = MsploitPostgres(user, password, db)
    for page in mpost.getwebpagesforhost(hostid):
        urlstring = "http"
        if "ssl" in page.get("protoname"):
            urlstring += "s"
        urlstring += "://{}:{}{}".format(ip,page.get("port"),page.get("path"))
        pageent = mt.addEntity("msploitego.SiteURL",urlstring)
        pageent.setValue(urlstring)
        pageent.addAdditionalFields("ip", "IP Address", False, ip)
        pageent.addAdditionalFields("hostid", "Host Id", False, hostid)
        for k,v in page.items():
            if isinstance(v,datetime):
                pageent.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                pageent.addAdditionalFields(k, k.capitalize(), False, str(v))

    for form in mpost.getwebformsforhost(hostid):
        urlstring = "http"
        if "ssl" in form.get("protoname"):
            urlstring += "s"
        urlstring += "://{}:{}{}".format(ip,form.get("port"),form.get("path"))
        forment = mt.addEntity("msploitego.WebForm",urlstring)
        forment.setValue(urlstring)
        for k,v in form.items():
            if isinstance(v,datetime):
                forment.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                forment.addAdditionalFields(k, k.capitalize(), False, str(v))
            forment.addAdditionalFields("ip", "IP Address", False, ip)

    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
