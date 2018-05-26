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
    rep = scriptrunner(port, "http-apache-negotiation,http-apache-server-status,http-vuln-cve2011-3192,http-vuln-cve2011-3368,http-vuln-cve2017-5638 ", ip)

    if rep.hosts[0].status == "up":
        for res in rep.hosts[0].services[0].scripts_results:
            cve = res.get("elements").popitem()
            if len(cve) > 0:
                apachevuln = mt.addEntity("msploitego.ApacheVulnerability", cve[0])
                apachevuln.setValue(cve[0])
                if isinstance(cve[1],dict):
                    details = cve[1]
                    for key,value in details.items():
                        if value and value.strip():
                            apachevuln.addAdditionalFields(key, key, False, value.strip())
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['httpapchevuln.py',
#  'http/80:294',
#  'properties.metasploitservice=http/80:294#info=Apache httpd 2.4.7 (Ubuntu)#name=http#proto=tcp#hostid=294#service.name=80/Apache 9#port=8080#banner=Apache 9#properties.service= #ip=10.10.10.61#state=open#fromfile=/root/data/scan/hthebox/msploitdb20180517.xml']
# dotransform(args)
