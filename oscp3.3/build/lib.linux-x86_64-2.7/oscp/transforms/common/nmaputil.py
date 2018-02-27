from libnmap.parser import NmapParser

from iptools.ip import IPAddress

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
    # TODO:allow any filename to be passed
    rep = NmapParser.parse_fromfile("/mnt/64G/proj/oscp-maltego/samplenmap.xml")
    #print "returning report"
    return rep

# ip = IPAddress("10.11.1.184")
# print type(ip)
# print type(ip.address)