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
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("address")
    hostid = mt.getVar("hostid")
    fn = mt.getValue()
    path = mt.getVar("path")

    bashlog = bashrunner("cat {}".format(path))
    details = "".join(bashlog)
    if details:
        fileent = mt.addEntity("msploitego.LootFile", fn)
        fileent.setValue(fn)
        fileent.addAdditionalFields("details", "Details", False, details)
        fileent.addAdditionalFields("ip", "IP Address", False, ip)

    mt.returnOutput()
    

dotransform(sys.argv)
# dotransform(args)