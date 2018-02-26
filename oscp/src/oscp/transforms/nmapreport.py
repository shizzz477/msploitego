from canari.maltego.entities import Unknown
from canari.maltego.transform import Transform
from canari.framework import EnableDebugWindow

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, oscp Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'


@EnableDebugWindow
class Nmapreport(Transform):
    """TODO: Your transform description."""

    # The transform input entity type.
    input_type = Unknown

    def do_transform(self, request, response, config):
        # TODO: write your code here.
        return response

    def on_terminate(self):
        """This method gets called when transform execution is prematurely terminated. It is only applicable for local
        transforms. It can be excluded if you don't need it."""
        pass