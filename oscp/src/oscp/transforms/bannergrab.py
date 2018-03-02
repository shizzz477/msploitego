#!/usr/bin/env python

from canari.maltego.utils import debug, progress
from canari.framework import configure #, superuser

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, Oscp Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

__all__ = [
    'dotransform',
    'onterminate' # comment out this line if you don't need this function.
]


"""
TODO: set the appropriate configuration parameters for your transform.
TODO: Uncomment the line below if the transform needs to run as super-user
"""
#@superuser
@configure(
    label='TODO: To Something [Hello World]',
    description='TODO: Returns a Something entity with the phrase "Hello Word!"',
    uuids=[ 'TODO something.v2.SomethingToPhrase_HelloWorld' ],
    inputs=[ ( 'TODO: Some Set', SomethingEntity ) ],
    debug=True
)
def dotransform(request, response, config):
    """
    TODO: write your data mining logic below.
    """
    return response


def onterminate():
    """
    TODO: Write your cleanup logic below or delete the onterminate function and remove it from the __all__ variable
    """
    pass