import unittest
import re
import types
from libnmap.objects import NmapReport

from msploitego.src.msploitego.transforms.common.nsescriptlib import scriptrunner

class TestNseLib(unittest.TestCase):

    def setUp(self):
        self.ip = "scanme.nmap.org"

    # using scanme.nmap.org
    def testsimplescan(self):
        rep = scriptrunner("80", "http-headers", self.ip)
        self.assertIsInstance(rep, NmapReport)
        self.assertIsNotNone(rep.hosts[0].services[0].scripts_results)
        rep = scriptrunner("80", "http-headers", self.ip, "-sS")
        self.assertIsInstance(rep, NmapReport)
        self.assertIsNotNone(rep.hosts[0].services[0].scripts_results)

    def testscanwithargs(self):
        rep = scriptrunner("80", "http-headers", self.ip, args="-sS", scriptargs="useget=1")
        self.assertIsInstance(rep, NmapReport)
        self.assertIsNotNone(rep.hosts[0].services[0].scripts_results)
        self.assertRegexpMatches(rep.commandline,"useget")

    def testscanNoPort(self):
        rep = scriptrunner(None,"banner",self.ip, args="-T4 -F")
        self.assertIsInstance(rep, NmapReport)
        self.assertEqual("up",rep.hosts[0].status)