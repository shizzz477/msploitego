import re
from pprint import pprint
from common.MaltegoTransform import *
from common.linuxtaskrunner import bashrunner

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
    mt.debug(pprint(args))
    mt.parseArguments(args)
    url = mt.getValue()
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    # gobuster -e -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://10.11.1.24/
    bashlog = bashrunner("gobuster -q -e -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u {}".format(url))
    for line in bashlog:
        webdir = mt.addEntity("maltego.WebDir", line.split()[0])
        webdir.setValue(line.split()[0])
        webdir.addAdditionalFields("ip", "IP Address", False, ip)
        webdir.addAdditionalFields("port", "Port", False, port)
        webdir.addAdditionalFields("url", "URL", False, url)

    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)
