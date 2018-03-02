import pprint
from libnmap.parser import NmapParser

from entities import Port, Service, OHost, Fingerprint, Vulnerability
from coreutil import listToDict, validVuln, sanitize
from entutil import createVulnerability

__author__ = 'Nadeem Douba'
__copyright__ = 'Copyright 2012, Sploitego Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Nadeem Douba'
__email__ = 'ndouba@gmail.com'
__status__ = 'Development'

# op = Port("139")
# op.portnumber = "139"
# op.servicename = "netbios"
# op.protocol = "tcp"
# op.source = "10.11.1.5"
# op.state = "open"

# pp = {"portnumber":"139", "servicename":"netbios", "protocol":"tcp", "source":"10.11.1.5", "state":"open"}

def getParsedReport(reportfilename):
    rep = NmapParser.parse_fromfile(reportfilename)
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

'''
{'CVE','State','VULNERABLE','date'}
'''
def doSmbVuln(vuln):
    if validVuln(vuln):
        d = listToDict(vuln)
        vulnerability = createVulnerability(d)
        return vulnerability
    else:
        return None
'''''

rep = getParsedReport("/mnt/64G/proj/oscp-maltego/bannersample.xml")
for _host in rep.hosts:
    pprint.pprint(_host)
    for s in _host.services:
        pprint.pprint(s)
        banner = s.banner
        print banner
        ban = ""
        bl = banner.split()
        if "product" in bl[0]:
            ban = " ".join(bl[1:])
        else:
            ban = banner
        print ban

for _host in rep.hosts:
    if _host.is_up():
        h = OHost(_host.ipv4)
        scripts = _host.scripts_results
        for res in scripts:
            if res.get('id') == "nbstat":
                print "handling nbstat script result: " + str(res)
            elif res.get('id') == "smb2-time":
                print "handling smb2-time script result: " + str(res)
            elif res.get('id') == "p2p-conficker":
                print "handling p2p-conficker script result: " + str(res)
            elif res.get('id') == "p2p-conficker":
                print "handling p2p-conficker script result: " + str(res)
            elif res.get('id') == "smb-os-discovery":
                print "handling smb-os-discovery script result: " + str(res)
            elif res.get('id') == "smb-security-mode":
                print "handling smb-security-mode script result: " + str(res)
            elif res.get('id') == "smb2-security-mode":
                print "handling smb2-security-mode script result: " + str(res)
            elif "smb-vuln" in res.get('id'):
                v = doSmbVuln(sanitize(res.get('output')))
                if v is not None:
                    pprint.pprint(v)
            else:
                print "** NO HANDLER for " + res.get('id')

        h.source = _host.ipv4
        h.mac = _host.mac
        h.vendor = _host.vendor
        for s in _host.services:
            # print str(s)
            if s.state == "open":
                op = Port(s.port)
                op.portnumber = s.port
                op.source = _host.address
                op.protocol = s.protocol
                op.state = s.state
                op.servicename = s.service
                op.banner = s.banner
                print "processed port: " + str(op)
        for os in _host.os.osmatches:
            fp = Fingerprint(os.name)
            fp.accuracy = str(os.accuracy)
            fp.osname = os.name
            print "processed figerprint: " + str(fp)
        print "processed host: "
        pprint.pprint(h)

 elif res.get('id') == "smb-vuln-cve2009-3103":
                print "handling smb-vuln-cve2009-3103 script result: " + str(res)
            elif res.get('id') == "smb-vuln-ms10-054":
                print "handling smb-vuln-ms10-054 script result: " + str(res)
            elif res.get('id') == "smb-vuln-ms10-061":
                print "handling smb-vuln-ms10-061 script result: " + str(res)
            elif res.get('id') == "smb-vuln-ms17-010":
                print "handling smb-vuln-ms17-010 script result: " + str(res)
            elif res.get('id') == "smb-vuln-ms08-067":
                print "handling smb-vuln-ms08-067 script result: " + str(res)
            elif res.get('id') == "smb-vuln-regsvc-dos":
                print "handling smb-vuln-regsvc-dos script result: " + str(res)

ads = host._address
for ad in ads:
    atype = ad.get('addrtype')
    if atype == "ipv4":
        print "handling address ipv4: " + ad.get('addr')
    if atype == "mac":
        print "handling mac: " + ad.get('addr')

# print str(host)
extras = host._extras
# print str(extras)
# hostscripts = extras['hostscripts']
# print str(hostscripts)
for key, value in extras.iteritems():
    print key + ":" + str(value)
    if key == "tcpsequence":
        print "handling tcpsequence: " + str(value)
    if key == "hostscript":
        print "handling hostscript: "  + str(value)
    if key == "extraports":
        print "handling extraports: "  + str(value)
    if key == "os":
        print "handling os: "  + str(value)
    if key == "ipidsequence":
        print "handling ipidsequence: "  + str(value)

results = host.get_field('script_results')
print str(results)

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