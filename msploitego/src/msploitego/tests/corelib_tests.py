import unittest
import re
import types
from pprint import pprint

from msploitego.src.msploitego.transforms.common.corelib import bucketparser, _nextheader


class Testcorelib(unittest.TestCase):

    def setUp(self):
        self.mylist1 = \
            [
                'HEADER01',
                'color:  blue',
                'cost:  100',
                'say:  hello',
                'HEADER02',
                'cost: 500',
                'say:  bye',
                'HEADER03',
                'race:  white',
                'size: small'
            ]
        self.reg1 = re.compile("^HEADER")

        self.mylist2 = ['', '  account_used: <blank>', '  \\\\10.11.1.24\\IPC$: ', '    Type: STYPE_IPC_HIDDEN',
                        '    Comment: IPC Service (payday server (Samba, Ubuntu))', '    Users: 1',
                        '    Max Users: <unlimited>', '    Path: C:\\tmp', '    Anonymous access: READ/WRITE',
                        '  \\\\10.11.1.24\\print$: ', '    Type: STYPE_DISKTREE_HIDDEN', '    Comment: Printer Drivers',
                        '    Users: 0', '    Max Users: <unlimited>', '    Path: C:\\var\\lib\\samba\\printers',
                        '    Anonymous access: <none>']
        self.reg2 = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

    def testbecketparse_core(self):
        tlist = ["HEADER01", "color: red-blue", "height: 5:6", "time: 10:30:12:PM",
                 'HEADER02', 'cost: 500', 'say:  bye'
                 ]
        results = bucketparser(self.reg1, tlist)
        self.assertIsInstance(results, list, "Expecting a results list")
        self.assertEqual(2, len(results), "Supposed to return 2 dict objects")
        for item in results:
            self.assertIsInstance(item, dict, "Expecting a dict item")
            header = item.get("Header")
            self.assertRegexpMatches(header, "HEADER")
            if header == "HEADER01":
                self.assertEqual(4, len(item), "This record should have 4 tags")
                self.assertEqual("10:30:12:PM", item.get("Time"), "Value of tag 'Time' not equal")
                self.assertEqual("5:6", item.get("Height"))
                self.assertEqual("red-blue", item.get("Color"))
            if header == "HEADER02":
                self.assertEqual(3, len(item), "This record should have 3 tags")
                self.assertEqual("500", item.get("Cost"))
                self.assertEqual("bye", item.get("Say"))

    def testbucketparse_match(self):
        results = bucketparser(self.reg1, self.mylist1)
        self.assertIsInstance(results, list, "Expecting a results list")
        self.assertEqual(3, len(results), "Supposed to return 3 dict objects")
        for item in results:
            self.assertIsInstance(item, dict, "Expecting a dict item")
            header = item.get("Header")
            self.assertRegexpMatches(header, "HEADER")
            if header == "HEADER01":
                self.assertIsNotNone(item.get("Color"))
                self.assertIsNotNone(item.get("Cost"))
                self.assertIsNotNone(item.get("Say"))
            if header == "HEADER02":
                self.assertIsNotNone(item.get("Cost"))
                self.assertIsNotNone(item.get("Say"))
            if header == "HEADER03":
                self.assertIsNotNone(item.get("Race"))
                self.assertIsNotNone(item.get("Size"))

    def testbucketparse_search(self):
        results = bucketparser(self.reg2, self.mylist2, method="search")
        self.assertIsInstance(results, list, "Expecting a results list")
        self.assertEqual(2, len(results), "Supposed to return 2 dict objects")
        for item in results:
            self.assertIsInstance(item, dict, "Expecting a dict item")
            header = item.get("Header")
            self.assertRegexpMatches(header, "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

    def testbucketspacesplit(self):
        l = ['',
             '  Backup Browser',
             '    OBSERVER  6.1  ',
             '    RALPH     5.2  ',
             '  DFS Root',
             '    MASTER  6.1  ',
             '    RALPH   5.2  ',
             '  Domain Controller',
             '    MASTER  6.1  ',
             '  Master Browser',
             '    RALPH  5.2  ',
             '  Potential Browser',
             '    ALICE     5.1  ',
             '    OBSERVER  6.1  ',
             '  SQL Server',
             '    RALPH  5.2  ',
             '  Server',
             '    RALPH  5.2  ',
             '    SLAVE  6.0  ',
             '  Server service',
             '    ALICE     5.1  ',
             '    MASTER    6.1  ',
             '    OBSERVER  6.1  ',
             '    RALPH     5.2  ',
             '    SLAVE     6.0  ',
             '  Windows NT/2000/XP/2003 server',
             '    ALICE     5.1  ',
             '    MASTER    6.1  ',
             '    OBSERVER  6.1  ',
             '    RALPH     5.2  ',
             '    SLAVE     6.0  ',
             '  Workstation',
             '    ALICE     5.1  ',
             '    MASTER    6.1  ',
             '    OBSERVER  6.1  ',
             '    RALPH     5.2  ',
             '    SLAVE     6.0  ',
             '']
        regex = re.compile("^\s{2}\w")
        results = bucketparser(regex, l, sep=" ")
        self.assertIsInstance(results, list, "Expecting a results list")
        self.assertEqual(10, len(results), "Supposed to return 10 dict objects")

    def testbucketparseCleanhttp(self):
        l = ['',
             '  VULNERABLE:',
             '  MS12-020 Remote Desktop Protocol Denial Of Service Vulnerability',
             '    State: VULNERABLE',
             '    IDs:  CVE:CVE-2012-0152',
             '    Risk factor: Medium  CVSSv2: 4.3 (MEDIUM) (AV:N/AC:M/Au:N/C:N/I:N/A:P)',
             '          Remote Desktop Protocol vulnerability that could allow remote attackers to cause a denial of service.',
             '          ',
             '    Disclosure date: 2012-03-13',
             '    References:',
             '      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-0152',
             '      http://technet.microsoft.com/en-us/security/bulletin/ms12-020',
             '  ',
             '  MS12-020 Remote Desktop Protocol Remote Code Execution Vulnerability',
             '    State: VULNERABLE',
             '    IDs:  CVE:CVE-2012-0002',
             '    Risk factor: High  CVSSv2: 9.3 (HIGH) (AV:N/AC:M/Au:N/C:C/I:C/A:C)',
             '          Remote Desktop Protocol vulnerability that could allow remote attackers to execute arbitrary code on the targeted system.',
             '          ',
             '    Disclosure date: 2012-03-13',
             '    References:',
             '      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2012-0002',
             '      http://technet.microsoft.com/en-us/security/bulletin/ms12-020',
             '']
        regex = re.compile("\s{2}[A-Za-z]+")
        results = bucketparser(regex, l)
        pprint(results)

# def nextheader(index,data,regex,method):
#     while index < len(data) and regex.match(data[index]) is None:
#         currline = data[index]
#         index += 1
#     return index