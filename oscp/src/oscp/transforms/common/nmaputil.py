from libnmap.parser import NmapParser

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'


def getParsedReport(reportfilename):
    #print reportfilename
    #
    rep = NmapParser.parse_fromfile("/mnt/64G/proj/oscp-maltego/sample02.xml")
    #print "returning report"
    return rep

def getHost(hostip):
    report = getParsedReport("file")
    for _host in report.hosts:
        if _host.address == hostip:
            return _host

# ip = IPAddress("10.11.1.184")
# print type(ip)
# print type(ip.address)

# _host = getHost("10.11.1.8")
# print _host


report = getParsedReport("some file")
for _host in report.hosts:
    if _host.is_up():
        mac = _host._mac_addr
''''
        if _host.os_fingerprinted:
            print("OS Fingerprint:")
            msg = ''
            for osm in _host.os.osmatches:
                print("Found Match:{0} ({1}%)".format(osm.name, osm.accuracy))
                for osc in osm.osclasses:
                    print("\tOS Class: {0}".format(osc.description))
                    for cpe in osc.cpelist:
                        print("\tCPE: {0}".format(cpe.cpestring))
'''''