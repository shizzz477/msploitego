import re
from pprint import pprint

from common.MaltegoTransform import *
import sys

from common.corelib import getFileContents, bucketparser
from common.linuxtaskrunner import bashrunner

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'marcgurreri@gmail.com'
__status__ = 'Development'

def packandroll(r):
    if r.get("Details"):
        d = r.get("Details")
    else:
        d = []
    for k, v in r.items():
        if not any(x in k for x in ["Header", "Details"]):
            d.append("{}  {}".format(k.strip(), v.strip()))
    return d

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(sys.argv))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    servicename = mt.getVar("servicename")
    serviceid = mt.getVar("serviceid")
    hostid = mt.getVar("hostid")
    workspace = mt.getVar("workspace")

    contents = bashrunner("")
    regex = re.compile("^\|\s+")
    ignore = re.compile("={3,}|Looking\s|padding\d|unknown_\d|logon_hrs|\[V\]\sAttempting\sto\sget|\*unknown\*|\[V\]\sassuming\sthat\suser|\[V\]\sprocessing\ssid\s|\[E\]", re.I)
    headsignore = re.compile("target\sinformation|getting\sprinter", re.I)
    results = bucketparser(regex,contents,ignoreg=ignore)
    for res in results:
        header = res.get("Header")
        if headsignore.search(header):
            continue
        if re.search("enumerating\sworkgroup",header,re.I):
            for k,v in res.items():
                if re.search("got\sdomain",k,re.I):
                    doment = mt.addEntity("maltego.Domain", v)
                    doment.setValue(v)
                    doment.addAdditionalFields("ip", "IP Address", True, ip)
                    doment.addAdditionalFields("hostid", "Host Id", True, hostid)
        elif re.search("nbtstat\sinformation",header,re.I):
            h = header.replace("|","").lstrip().rstrip()
            nbstat = mt.addEntity("msploitego.nbstatinformation",h)
            nbstat.setValue(h)
            nbstat.addAdditionalFields("data", "Data", False, "\n".join(res.get("Details")))
            nbstat.addAdditionalFields("ip", "IP Address", True, ip)
            nbstat.addAdditionalFields("hostid", "Host Id", True, hostid)
        elif re.search("session\scheck\son",header,re.I):
            data = packandroll(res)
            if data:
                h = header.replace("|", "").lstrip().rstrip()
                sessioncheck = mt.addEntity("msploitego.nbstatinformation",h)
                sessioncheck.setValue(h)
                sessioncheck.addAdditionalFields("data", "Data", False, "\n".join(data))
                sessioncheck.addAdditionalFields("ip", "IP Address", True, ip)
                sessioncheck.addAdditionalFields("hostid", "Host Id", True, hostid)
        elif re.search("getting\sdomain\ssid",header,re.I):
            data = packandroll(res)
            if data:
                h = header.replace("|", "").lstrip().rstrip()
                domainsid = mt.addEntity("msploitego.RelevantInformation", h)
                domainsid.setValue(h)
                domainsid.addAdditionalFields("data", "Data", False, "\n".join(data))
                domainsid.addAdditionalFields("ip", "IP Address", True, ip)
                domainsid.addAdditionalFields("hostid", "Host Id", True, hostid)
        elif re.search("os\sinformation\son",header,re.I):
            data = packandroll(res)
            if data:
                h = header.replace("|", "").lstrip().rstrip()
                osinfo = mt.addEntity("msploitego.SambaOSInformation", h)
                osinfo.setValue(h)
                osinfo.addAdditionalFields("data", "Data", False, "\n".join(data))
                osinfo.addAdditionalFields("ip", "IP Address", True, ip)
                osinfo.addAdditionalFields("hostid", "Host Id", True, hostid)
        elif re.search("\svia\srid\scyling",header,re.I):
            data = packandroll(res)
            if data:
                h = header.replace("|", "").lstrip().rstrip()
                ridinfo = mt.addEntity("msploitego.SambaAccountInformation", h)
                ridinfo.setValue(h)
                ridinfo.addAdditionalFields("data", "Data", False, "\n".join(data))
                ridinfo.addAdditionalFields("ip", "IP Address", True, ip)
                ridinfo.addAdditionalFields("hostid", "Host Id", True, hostid)
        elif re.search("\susers\son\s",header,re.I):
            data = packandroll(res)
            if data:
                h = header.replace("|", "").lstrip().rstrip()
                userinfo = mt.addEntity("msploitego.SambaAccountInformation", h)
                userinfo.setValue(h)
                userinfo.addAdditionalFields("data", "Data", False, "\n".join(data))
                userinfo.addAdditionalFields("ip", "IP Address", True, ip)
                userinfo.addAdditionalFields("hostid", "Host Id", True, hostid)
        elif re.search("\smacine\senumeration\s",header,re.I):
            data = packandroll(res)
            if data:
                h = header.replace("|", "").lstrip().rstrip()
                machineinfo = mt.addEntity("msploitego.SambaMachineEnumeration", h)
                machineinfo.setValue(h)
                machineinfo.addAdditionalFields("data", "Data", False, "\n".join(data))
                machineinfo.addAdditionalFields("ip", "IP Address", True, ip)
                machineinfo.addAdditionalFields("hostid", "Host Id", True, hostid)
        elif re.search("\sshare\senumeration\son\s",header,re.I):
            data = packandroll(res)
            if data:
                h = header.replace("|", "").lstrip().rstrip()
                shareinfo = mt.addEntity("msploitego.SambaShareInformation", h)
                shareinfo.setValue(h)
                shareinfo.addAdditionalFields("data", "Data", False, "\n".join(data))
                shareinfo.addAdditionalFields("ip", "IP Address", True, ip)
                shareinfo.addAdditionalFields("hostid", "Host Id", True, hostid)
        elif re.search("\spassword\spolicy\sinformation\s",header,re.I):
            data = packandroll(res)
            if data:
                h = header.replace("|", "").lstrip().rstrip()
                passinfo = mt.addEntity("msploitego.SambaPasswordPolicyInfo", h)
                passinfo.setValue(h)
                passinfo.addAdditionalFields("data", "Data", False, "\n".join(data))
                passinfo.addAdditionalFields("ip", "IP Address", True, ip)
                passinfo.addAdditionalFields("hostid", "Host Id", True, hostid)
        elif re.search("\sgroups\son\s",header,re.I):
            data = packandroll(res)
            if data:
                h = header.replace("|", "").lstrip().rstrip()
                passinfo = mt.addEntity("msploitego.SambaGroupInformation", h)
                passinfo.setValue(h)
                passinfo.addAdditionalFields("data", "Data", False, "\n".join(data))
                passinfo.addAdditionalFields("ip", "IP Address", True, ip)
                passinfo.addAdditionalFields("hostid", "Host Id", True, hostid)
    mt.returnOutput()

dotransform(sys.argv)
# dotransform(args)