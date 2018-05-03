import unittest

from canari.maltego.message import MaltegoTransformRequestMessage
from canari.maltego.entities import File

from msploitego.src.msploitego.transforms.common.entities import Host
from msploitego.src.msploitego.transforms.common.msploitdb import MetasploitXML, Mhost


class Testmsploitdb(unittest.TestCase):

    def setUp(self):
        self.file = File("/root/data/scan/hthebox/msploitdb20180501.xml")

    def testreqmessage(self):
        req = MaltegoTransformRequestMessage()
        req.__iadd__(self.file)
        self.assertIsInstance(req.entity, File)
        self.assertTrue(req.entity.value == "/root/data/scan/hthebox/msploitdb20180501.xml")

    def testmetasploitxml(self):
        mdb = MetasploitXML(self.file)
        self.assertIsNotNone(mdb)

    def testhostsmaltego(self):
        mdb = MetasploitXML(self.file)
        for h in mdb.hosts:
            self.assertIsInstance(h, Mhost)
            self.assertIsInstance(h.maltego(), Host)