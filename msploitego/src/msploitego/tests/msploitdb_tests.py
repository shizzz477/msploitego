import unittest

import types
from msploitego.src.msploitego.transforms.common.corelib import SimpleElement, Melement
from msploitego.src.msploitego.transforms.common.msploitdb import MetasploitXML, Mhost, Mservice


class Testmsploitdb(unittest.TestCase):

    def setUp(self):
        self.filename = "/root/data/scan/hthebox/msploitdb-20180508.xml"
        self.mdb = MetasploitXML(self.filename)

    def testMetasploitXML(self):
        self.assertIsNotNone(self.mdb)
        self.assertIsInstance(self.mdb.hosts, types.GeneratorType)
        self.assertIsInstance(self.mdb.services, types.GeneratorType)
        self.assertIsInstance(self.mdb.hosts, types.GeneratorType)

    def testMHost(self):
        mhost = self.mdb.hosts.next()
        self.assertIsInstance(mhost, SimpleElement)
        self.assertIsInstance(mhost, Mhost)
        self.assertGreater(len(mhost._dict),0)
        self.assertIsInstance(mhost.services, types.GeneratorType)
        self.assertIsInstance(mhost.notes, types.GeneratorType)
        if mhost.vulns:
            self.assertIsInstance(mhost.vulns, types.GeneratorType)

    def testservice(self):
        mservice = self.mdb.hosts.next().services.next()
        self.assertIsInstance(mservice, SimpleElement)
        self.assertIsInstance(mservice, Melement)
        self.assertIsInstance(mservice, Mservice)
        self.assertGreater(len(mservice._dict), 0)
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

 #    def testdotransform(self):
 #        req = ['metasploitdb.py',
 # '/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/msploitdb20180501.xml',
 # 'description=/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/msploitdb20180501.xml']
 #        ret = dotransform(req)
 #        print "returned"
        # req.__iadd__(self.file)
        # transform = Metasploitdb()
        # transform.do_transform(req, MaltegoTransformResponseMessage(), load_config(self.canariconf))