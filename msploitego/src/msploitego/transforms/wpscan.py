import re
from pprint import pprint
from common.MaltegoTransform import *
from common.linuxtaskrunner import bashrunner
from common.corelib import bucketparser

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

    bashlog = bashrunner("wpscan --url {}:{} --enumerate p,u --no-banner --no-color".format(ip,port))
    regex = re.compile("^\[!\]")
    results = bucketparser(regex, bashlog)

    for res in results:
        print "test"
    mt.returnOutput()

# dotransform(sys.argv)
args = ['wpscan.py',
 'http/80:524',
 'properties.metasploitservice=http/80:524#info=Apache/2.2.14 (Ubuntu) ( Powered by PHP/5.3.2-1ubuntu4 )#proto=tcp#hostid=524#service.name=http/80:524#port=80#banner=Apache/2.2.14 (Ubuntu) ( Powered by PHP/5.3.2-1ubuntu4 )#properties.service= #workspace=default#ip=10.11.1.234#created_at=24/2/2018#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#updated_at=31/5/2018#machinename=10.11.1.234#servicename=http#state=open#serviceid=6859#user=msf#db=msf#workspaceid=18']
dotransform(args)
