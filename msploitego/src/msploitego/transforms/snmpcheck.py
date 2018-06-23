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
__email__ = 'marcgurreri@gmail.com'
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
            phrase = mt.addEntity("msploitego.RelevantInformation", "{}:{}".format(origheader,hostid))
            phrase.setValue("{}:{}".format(origheader,hostid))
        elif "system information" in header:
            if res.get("Domain"):
                dname = res.get("Domain").lstrip(":")
                domain = mt.addEntity("maltego.Domain", dname)
                domain.setValue(dname)
                domain.addAdditionalFields("ip", "IP Address", True, ip)
                domain.addAdditionalFields("port", "Port", True, port)
            if res.get("Hostname"):
                hname = res.get("Hostname").lstrip(":")
                hostname = mt.addEntity("msploitego.Hostname", hname)
                hostname.setValue(hname)
                hostname.addAdditionalFields("ip", "IP Address", True, ip)
                hostname.addAdditionalFields("port", "Port", True, port)
        elif "user accounts" in header:
            for user in res.keys():
                if any(x in user for x in ["Details", "Header"]):
                    continue
                alias = mt.addEntity("maltego.Alias", user)
                alias.setValue(user)
                alias.addAdditionalFields("ip", "IP Address", True, ip)
        elif "routing information" in header:
            ipprefix = ".".join(ip.split(".")[0:2])
            for k,v in res.items():
                if any(x in k for x in ["Details", "Header","Destination"]):
                    continue
                for ipr in v.split():
                    if re.search(ipprefix,ipr) and ipr != ip:
                        iprout = mt.addEntity("msploitego.RoutingIP", ipr)
                        iprout.setValue(ipr)
                        iprout.addAdditionalFields("ip", "IP Address", True, ip)
        elif "network services" in header:
            for k,v in res.items():
                if any(x in k for x in ["Details", "Header","Index"]):
                    continue
                nservice = mt.addEntity("msploitego.NetworkService", "{}:{}".format(v,hostid))
                nservice.setValue("{}:{}".format(v,hostid))
                nservice.addAdditionalFields("ip", "IP Address", True, ip)
        elif "processes" in header:
            for k,v in res.items():
                if any(x in k for x in ["Details", "Header"]):
                    continue
                if "running" in v.lower():
                    process = mt.addEntity("msploitego.Process", "{}:{}".format(v.split()[-1],hostid))
                    process.setValue("{}:{}".format(v.split()[-1],hostid))
                    process.addAdditionalFields("ip", "IP Address", True, ip)
                    process.addAdditionalFields("pid","Process ID", True, k)
        elif "device information" in header:
            for k,v in res.items():
                if any(x in k for x in ["Details", "Header", "Id"]):
                    continue
                if any(x in v for x in ["unknown","running"]):
                    device = mt.addEntity("maltego.Device", "{}:{}".format(" ".join(v.split()[2::]),hostid))
                    device.setValue("{}:{}".format(" ".join(v.split()[2::]),hostid))
                    device.addAdditionalFields("ip", "IP Address", True, ip)
        elif "software components" in header:
            for k,v in res.items():
                if any(x in k for x in ["Details","Index","Header"]):
                    continue
                iprout = mt.addEntity("msploitego.SotwareComponents", "{}:{}".format(v,hostid))
                iprout.setValue("{}:{}".format(v,hostid))
                iprout.addAdditionalFields("ip", "IP Address", True, ip)
        elif "share" in header:
            path = res.get("Path").lstrip(":")
            name = res.get("Name").lstrip(":")
            networkshare = mt.addEntity("msploitego.NetworkShare", path)
            networkshare.setValue(path)
            networkshare.addAdditionalFields("ip", "IP Address", True, ip)
            networkshare.addAdditionalFields("name", "Share Name", True, name)

    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)
