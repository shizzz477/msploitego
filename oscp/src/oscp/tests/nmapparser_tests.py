import unittest
import types
from libnmap.parser import NmapParser

from oscp.src.oscp.transforms.common.nmapparser import Nmapreport, Nhost, Nservice

class Testnmapparser(unittest.TestCase):
    def setUp(self):
        self.nmap = Nmapreport("/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/zenmap-oscp-scan.xml")

    def test_hosts(self):
        self.assertIsInstance(self.nmap.hosts, types.GeneratorType)
    def test_host(self):
        h = self.nmap.hosts.next()
        self.assertIsInstance(h, Nhost)
        self.assertIsInstance(h.osmatches, types.GeneratorType)

    def test_service(self):
        services = self.nmap.hosts.next().services
        self.assertIsInstance(services, types.GeneratorType)
        s = services.next()
        self.assertIsInstance(s, Nservice)
        self.assertTrue(s.state.lower() == "open")
    def test_service_required(self):
        s = self.nmap.hosts.next().services.next()
        self.assertIsNotNone(s.port)