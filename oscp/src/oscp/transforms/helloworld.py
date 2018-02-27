#!/usr/bin/env python

from canari.maltego.entities import Person
from canari.maltego.utils import debug, progress
from canari.framework import configure #, superuser
from common.entities import MyOscpEntity

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
    'onterminate'
]

# Uncomment the line below if the transform needs to run as super-user
#@superuser
"""
The @configure decorator tells mtginstall how to install the transform in Maltego. It takes the following parameters:
    - label:        the name of the transform as it appears in the Maltego UI transform selection menu
    - description:  a short description of the transform
    - uuids:        a list of unique transform IDs, one per input type. The order of this list must match that of the 
                    inputs parameter. Make sure you account for entity type inheritance in Maltego. For example, if you
                    choose a DNSName entity type as your input type you do not need to specify it again for MXRecord, 
                    NSRecord, etc.
    - inputs:       a list of tuples where the first item is the name of the transform set the transform should be part
                    of, and the second item is the input entity type.
    - debug:        Whether or not the debugging window should appear in Maltego's UI when running the transform.
    - remote:       Whether or not the transform can be used as a remote transform in Plume.
TODO: set the appropriate configuration parameters for your transform.
"""
@configure(
    label='To MyOscpEntity [Hello World]',
    description='Returns a MyOscpEntity entity with the phrase "Hello Word!"',
    uuids=[ 'oscp.v2.MyOscpEntityToPhrase_HelloWorld' ],
    inputs=[ ( 'Oscp', Person ) ],
    remote=False,
    debug=True
)
def dotransform(request, response, config):
    """
    The dotransform function is our transform's entry point. The request object has the following properties:
        - value:    a string containing the value of the input entity.
        - fields:   a dictionary of entity field names and their respective values of the input entity.
        - params:   any additional command-line arguments to be passed to the transform.
        - entity:   the information above is serialized into an Entity object. The entity type is determined
                    by the inputs field in @configure for local transforms. For remote transforms, the entity
                    type is determined by the information in the body of the request. Local transforms suffer
                    from one limitation: if more than one entity type is listed in the inputs field of @configure,
                    the entity type might not be resolvable. Therefore, this should not be referenced in local
                    transforms if there is more than one input entity type defined in @configure.

    The response object is a container for output entities, UI messages, and exception messages. The config object
    contains a key-value store of the configuration file.
    TODO: write your data mining logic below.
    """

    # Report transform progress
    progress(50)
    # Send a debugging message to the Maltego UI console
    debug('This was pointless!')

    # Create MyOscpEntity entity with value set to 'Hello <request.value>!'
    e = MyOscpEntity('Hello %s!' % request.value)
    # Setting field values on the entity
    e.field1 = 2
    e.fieldN = 'test'
    # Update progress
    progress(100)

    # Add entity to response object
    response += e

    # Return response for visualization
    return response


"""
Called if transform interrupted. It's presence is optional; you can remove this function if you don't need to do any
resource clean up.

TODO: Write your cleanup logic below or delete the onterminate function and remove it from the __all__ variable 
"""
def onterminate():
    debug('Caught signal... exiting.')
    exit(0)