from pprint import pprint
from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *

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
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    rep = scriptrunner(port, "smtp-enum-users", ip)

    for res in rep.hosts[0].services[0].scripts_results:
        output = res.get("output")
        for username in output.split(","):
            username = username.strip().lstrip()
            userentity = mt.addEntity("maltego.Alias", username)
            userentity.setValue(username)
            userentity.addAdditionalFields("sourceip", "Source IP", False, ip)
            userentity.addAdditionalFields("sourceport", "Source Port", False, port)
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['smtpenumusers.py',
#  'smtp/25:298',
#  'properties.metasploitservice=smtp/25:298#info=JAMES smtpd 2.3.2#name=smtp#proto=tcp#hostid=298#service.name=80/Apache 9#port=25#banner=Apache 9#properties.service= #ip=10.10.10.51#state=open#fromfile=/root/data/scan/hthebox/msploitdb20180517.xml']
# dotransform(args)
