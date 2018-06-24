from pprint import pprint

from common.MaltegoTransform import *
from common.corelib import inheritvalues

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
    noteon = mt.getValue()
    noteent = mt.addEntity("msploitego.Note", "Note:{}".format(noteon))
    noteent.setValue("Note:{}".format(noteon))
    noteent.addAdditionalFields("note", "Note", False, "")
    noteent.addAdditionalFields("link", "Link", False, "")
    inheritvalues(noteent,mt.values)
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
