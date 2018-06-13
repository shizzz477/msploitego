import unittest
from pprint import pprint
import types
from msploitego.src.msploitego.transforms.common.postgresdb import MsploitPostgres
import psycopg2
import psycopg2.extras

class TestPostgresDb(unittest.TestCase):

    def setUp(self):
        self.mpost = MsploitPostgres("msf","msf", "msf")
        self.assertIsNotNone(self.mpost)

    def tearDown(self):
        pass

    def testAllhostsquery(self):
        hosts = self.mpost.getAllHosts()
        self.assertIsNotNone(hosts)

    # def testhostquery(self):
    #     hostgen = self.mpost.getHost()
    #     self.assertIsInstance(hostgen,types.GeneratorType)
    #     for host in hostgen:
    #         self.assertIsInstance(host.keys(), list)

    def testlootforhost(self):
        pass