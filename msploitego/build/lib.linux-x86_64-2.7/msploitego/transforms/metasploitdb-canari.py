from canari.maltego.entities import File
from canari.maltego.transform import Transform
from canari.framework import EnableDebugWindow

from msploitego.src.msploitego.transforms.common.entities import Host
from msploitego.src.msploitego.transforms.common.msploitdb import MetasploitXML

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

@EnableDebugWindow
class Metasploitdb(Transform):
    """Parse a Metasploit database into Maltego entities."""

    # The transform input entity type.
    input_type = File

    def do_transform(self, request, response, config):
        fname = request.entity
        mdb = MetasploitXML(fname.value)
        for h in mdb.hosts:
            response += h.tomaltego()
        return response

    def on_terminate(self):
        """This method gets called when transform execution is prematurely terminated. It is only applicable for local
        transforms. It can be excluded if you don't need it."""
        pass