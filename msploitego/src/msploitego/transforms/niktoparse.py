from common.MaltegoTransform import *
from common.niktolib import NiktoReport
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
    # mt.debug(pprint(sys.argv))
    mt.parseArguments(sys.argv)
    fn = mt.getVar("niktofile")
    if not fn:
        mt.addException("Nikto file is either not attached or does not exist")
        mt.returnOutput()
    else:
        nr = NiktoReport(fn)
        for d in nr.details:
            det = mt.addEntity("msploitego.niktodetail", d.description)
            det.setValue(d.description[0:25])
            det.addAdditionalFields("description","Description",False,d.description)
            det.addAdditionalFields("iplink", "IP Link", False, d.iplink)
            det.addAdditionalFields("namelink", "Name Link", False, d.namelink)
            det.addAdditionalFields("uri", "URI", False, d.uri)
        mt.returnOutput()
        mt.addUIMessage("completed!")

# dotransform(sys.argv)
args = ['niktoparse.py',
 'http/80',
 'service.name=http/80#port=80#banner=Apache 9#properties.service= #ip=10.10.10.63#niktofile=/root/proj/oscp-maltego/msploitego/src/msploitego/resources/10.11.1.22-80.xml#fromfile=/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/msploitdb20180501.xml#info=Microsoft IIS httpd 10.0#name=http#proto=tcp#state=open']
dotransform(args)