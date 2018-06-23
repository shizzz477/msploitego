from pprint import pprint
import webbrowser
import os

import validators
from common.MaltegoTransform import *

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
    filenmame = mt.getVar("localfile")
    if filenmame:
        if os.path.exists(filenmame):
            webbrowser.open("file://{}".format(filenmame))
    else:
        url = mt.getValue()
        if validators.url(url):
            webbrowser.open(url)
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
