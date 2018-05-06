import unittest

from canari.maltego.message import MaltegoTransformRequestMessage, MaltegoTransformResponseMessage
from canari.maltego.entities import File

from msploitego.src.msploitego.transforms.common.entities import Host
from msploitego.src.msploitego.transforms.common.msploitdb import MetasploitXML, Mhost
from msploitego.src.msploitego.transforms.metasploitdb import dotransform

class Testmsploitdb(unittest.TestCase):

    def setUp(self):
        self.file = File("/root/data/scan/hthebox/msploitdb20180501.xml")
        # self.canariconf = "/usr/local/lib/python2.7/dist-packages/canari-3.2.2-py2.7.egg/canari/resources/etc/canari.conf"

    # def testreqmessage(self):
    #     req = MaltegoTransformRequestMessage()
    #     req.__iadd__(self.file)
    #     self.assertIsInstance(req.entity, File)
    #     self.assertTrue(req.entity.value == "/root/data/scan/hthebox/msploitdb20180501.xml")

    # def testmetasploitxml(self):
    #     mdb = MetasploitXML(self.file)
    #     self.assertIsNotNone(mdb)

    # def testhostsmaltego(self):
    #     mdb = MetasploitXML(self.file)
    #     for h in mdb.hosts:
    #         self.assertIsInstance(h, Mhost)
    #         self.assertIsInstance(h.maltego(), Host)

    def testdotransform(self):
        req = ['metasploitdb.py',
 '/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/msploitdb20180501.xml',
 'description=/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/msploitdb20180501.xml']
        ret = dotransform(req)
        print "returned"
        # req.__iadd__(self.file)
        # transform = Metasploitdb()
        # transform.do_transform(req, MaltegoTransformResponseMessage(), load_config(self.canariconf))