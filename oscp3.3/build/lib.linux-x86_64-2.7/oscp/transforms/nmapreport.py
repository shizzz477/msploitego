from canari.maltego.entities import File, Phrase, IPv4Address
from canari.maltego.transform import Transform
from canari.framework import EnableDebugWindow

from common.nmaputil import getParsedReport
from common.entities import Oport
from sploitego.transforms.common.entities import Port

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, oscp Project'
__credits__ = []

__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

filepath = "/mnt/64G/proj/oscp-maltego/samplenmap.xml"

@EnableDebugWindow
class Nmapreport(Transform):
    """Takes a string as a filename and parses nmap report"""

    # The transform input entity type.
    input_type = Phrase

    def do_transform(self, request, response, config):
        nmapfile = request.entity
        #filepath = nmapfile.source
        #print filepath
        parsedreport = getParsedReport(filepath)
        for _host in parsedreport.hosts:
            if _host.is_up():
                ipaddr = IPv4Address(_host.address)
                response += ipaddr
        return response

    def on_terminate(self):
        """This method gets called when transform execution is prematurely terminated. It is only applicable for local
        transforms. It can be excluded if you don't need it."""
        pass

@EnableDebugWindow
class EnumPorts(Transform):
    """OSCP Enum Ports"""
    input_type = IPv4Address

    def do_transform(self, request, response, config):
        ipv4obj = request.entity
        ip = ipv4obj.value
        # print "IP retrieved from request entity " + ip
        parsedreport = getParsedReport(filepath)
        for _host in parsedreport.hosts:
            # print "checking host: " + _host.address
            # print type(ip)
            if _host.address == ip:
                for s in _host.services:
                    # print "found service"
                    # print s
                    # s.port,s.protocol,s.state
                    op = Port(s.port)
                    # op = Oport(s.port)
                    op.ip.destination = _host.address
                    op.protocol = s.protocol
                    op.port.status = s.state
                    # print op
                    response += op
        return response

    def on_terminate(self):
        pass