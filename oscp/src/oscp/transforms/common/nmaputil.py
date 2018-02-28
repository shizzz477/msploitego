from libnmap.parser import NmapParser

from entities import Port, Service

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

op = Port("139")
op.portnumber = "139"
op.servicename = "netbios"
op.protocol = "tcp"
op.source = "10.11.1.5"
op.state = "open"

pp = {"portnumber":"139", "servicename":"netbios", "protocol":"tcp", "source":"10.11.1.5", "state":"open"}

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

def getService(h, p):
    hst = getHost(h)
    for srv in hst.services:
        if srv.port == p:
            return srv

# ip = IPAddress("10.11.1.184")
# print type(ip)
# print type(ip.address)

# _host = getHost("10.11.1.8")
# print _host

# host = getHost("10.11.1.5")
'''''

s = getService("10.11.1.5", 139)
print str(s)
ps = Service(pp['servicename'])
ps.servicename = pp['servicename']
ps.portnumber = pp['portnumber']
print str(ps)
print str(op)
#  for s in host.services:

report = getParsedReport("some file")
for _host in report.hosts:
    if _host.is_up():
         #hostosinfo = (_host.address, 0, "OS")
        if _host.address == "10.11.1.5":
            for s in _host.services:
                op = Port(s.port)
                #if op.status == "open":
                op.source = _host.address
                op.protocol = s.protocol
                op.state = s.state
                serviced = s._service
                op.servicename = serviced['name']
                op.product = serviced['product']
                print str(op)

report = getParsedReport("some file")
for _host in report.hosts:
    if _host.is_up():
         #hostosinfo = (_host.address, 0, "OS")
        if _host.address == "10.11.1.5":
            for os in _host.os.osmatches:
                #port = os.portused
                print "OSM: " + str(os)
                accuracy = os.accuracy
                osname = os.name
                # if accuracy >
                print "accuracy: " + str(accuracy) + " name: " + osname
'''''
'''''
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