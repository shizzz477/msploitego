import re
from pprint import pprint
from common.MaltegoTransform import *
from common.linuxtaskrunner import bashrunner
from common.corelib import bucketparser

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")

    bashlog = bashrunner("snmp-check -w {}".format(ip))
    regex = re.compile("^\[\*\]")
    results = bucketparser(regex, bashlog, sep=" ")

    for res in results:
        origheader = res.get("Header")
        header = res.get("Header").lower()
        if "write access permitted" in header:
            phrase = mt.addEntity("maltego.Pharse", origheader)
            phrase.setValue(origheader)
        elif "system information" in header:
            if res.get("Domain"):
                dname = res.get("Domain").lstrip(":")
                domain = mt.addEntity("maltego.Domain", dname)
                domain.setValue(dname)
                domain.addAdditionalFields("ip", "IP Address", False, ip)
                domain.addAdditionalFields("port", "Port", False, port)
            if res.get("Hostname"):
                hname = res.get("Hostname").lstrip(":")
                hostname = mt.addEntity("msploitego.Hostname", hname)
                hostname.setValue(hname)
                hostname.addAdditionalFields("ip", "IP Address", False, ip)
                hostname.addAdditionalFields("port", "Port", False, port)
        elif "user accounts" in header:
            for user in res.keys():
                if any(x in user for x in ["Details", "Header"]):
                    continue
                alias = mt.addEntity("maltego.Alias", user)
                alias.setValue(user)
                alias.addAdditionalFields("ip", "IP Address", False, ip)
        # elif "network interfaces" in header:
        #     if res.get("Interface"):
        #         iname = res.get("Interface").lstrip(":")
        #         ninterface = mt.addEntity("msploitego.NetworkInterface", iname)
        #         ninterface.setValue(iname)
        #         ninterface.addAdditionalFields("ip", "IP Address", False, ip)
        #     if res.get("Mac"):
        #         m = res.get("Mac").split(":",1)[-1].lstrip()
        #         mac = mt.addEntity("maltego.MacAddress", m)
        #         mac.setValue(m)
        elif "routing information" in header:
            ipprefix = ".".join(ip.split(".")[0:2])
            for k,v in res.items():
                if any(x in k for x in ["Details", "Header","Destination"]):
                    continue
                for ipr in v.split():
                    if re.search(ipprefix,ipr) and ipr != ip:
                        iprout = mt.addEntity("maltego.MacAddress", v)
                        iprout.setValue(v)
                        iprout.addAdditionalFields("ip", "IP Address", False, ipr)
        elif "network services" in header:
            for k,v in res.items():
                if any(x in k for x in ["Details", "Header","Index"]):
                    continue
                nservice = mt.addEntity("msploitego.NetworkService", v)
                nservice.setValue(v)
                nservice.addAdditionalFields("ip", "IP Address", False, ip)
        elif "processes" in header:
            for k,v in res.items():
                if any(x in k for x in ["Details", "Header"]):
                    continue
                if "running" in v.lower():
                    process = mt.addEntity("msploitego.Process", v.split()[-1])
                    process.setValue(v.split()[-1])
                    process.addAdditionalFields("ip", "IP Address", False, ip)
                    process.addAdditionalFields("pid","Process ID", False, k)
        elif "device information" in header:
            for k,v in res.items():
                if any(x in k for x in ["Details", "Header", "Id"]):
                    continue
                if any(x in v for x in ["unknown","running"]):
                    device = mt.addEntity("maltego.Device", " ".join(v.split()[2::]))
                    device.setValue(" ".join(v.split()[2::]))
                    device.addAdditionalFields("ip", "IP Address", False, ip)
        elif "software components" in header:
            for k,v in res.items():
                if any(x in k for x in ["Details","Index","Header"]):
                    continue
                iprout = mt.addEntity("msploitego.SotwareComponents", v)
                iprout.setValue(v)
                iprout.addAdditionalFields("ip", "IP Address", False, ip)
        elif "share" in header:
            path = res.get("Path").lstrip(":")
            name = res.get("Name").lstrip(":")
            networkshare = mt.addEntity("msploitego.NetworkShare", path)
            networkshare.setValue(path)
            networkshare.addAdditionalFields("ip", "IP Address", False, ip)
            networkshare.addAdditionalFields("name", "Share Name", False, name)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['snmpcheck.py',
#  'snmp/161:516',
#  'properties.metasploitservice=snmp/161:516#name=snmp#proto=udp#hostid=516#service.name=snmp#port=161#banner=snmp-No info#properties.service= #ip=10.11.1.227#state=open#fromfile=/root/data/report_pack/msploitdb20180524.xml']
# dotransform(args)
