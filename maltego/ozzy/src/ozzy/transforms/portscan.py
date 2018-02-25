from canari.maltego.entities import IPv4Address
from canari.maltego.transform import Transform
from canari.framework import EnableDebugWindow

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, ozzy Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'


@EnableDebugWindow
class Portscan(Transform):
    """Do a first level port scan"""

    # The transform input entity type.
    input_type = IPv4Address

    def do_transform(self, request, response, config):
        # TODO: write your code here.
        return response

    def on_terminate(self):
        """This method gets called when transform execution is prematurely terminated. It is only applicable for local
        transforms. It can be excluded if you don't need it."""
        pass