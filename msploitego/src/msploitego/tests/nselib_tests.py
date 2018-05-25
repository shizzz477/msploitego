import unittest
import re
import types
from libnmap.objects import NmapReport

from msploitego.src.msploitego.transforms.common.nsescriptlib import scriptrunner

class TestNseLib(unittest.TestCase):

    # using scanme.nmap.org
    def testsimplescan(self):
        rep = scriptrunner("80", "http-headers", "45.33.32.156")
        self.assertIsInstance(rep, NmapReport)
        self.assertIsNotNone(rep.hosts[0].services[0].scripts_results)
        rep = scriptrunner("80", "http-headers", "45.33.32.156", "-sS")
        self.assertIsInstance(rep, NmapReport)
        self.assertIsNotNone(rep.hosts[0].services[0].scripts_results)

    def testscanwithargs(self):
        rep = scriptrunner("80", "http-headers", "45.33.32.156", "-sS", "useget=1")
        self.assertIsInstance(rep, NmapReport)
        self.assertIsNotNone(rep.hosts[0].services[0].scripts_results)
        self.assertRegexpMatches(rep.commandline,"useget")