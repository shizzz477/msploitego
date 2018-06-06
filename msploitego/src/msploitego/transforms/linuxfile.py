from pprint import pprint
from common.MaltegoTransform import *
from common.linuxtaskrunner import bashrunner

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
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['linuxfile.py',
#  'cnpilot_snmp_loot.txt',
# 'properties.metasploitloot=cnpilot_snmp_loot.txt#info=Cambium cnPilot configuration data#ltype=snmp_loot#workspace_id=18#created_at=31/5/2018#address=10.11.1.14#updated_at=31/5/2018#content_type=text/plain#host_id=537#path=/root/.msf4/loot/20180531131742_default_10.11.1.14_snmp_loot_022307.txt#id=137#name=cnpilot_snmp_loot.txt#user=msf#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\=#db=msf']
# dotransform(args)