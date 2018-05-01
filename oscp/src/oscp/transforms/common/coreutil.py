import pprint
import re





errormsgs = [
    "ERROR:",
    "could not connect",
    "system is patched",
    "OBJECT_NAME_NOT_FOUND",
    "Sorry!",
    "ACCESS_DENIED"
]
# assumes key sep is colon, item sep is space
def listToDict(o):
    l = re.split(': +', o)
    key = l[0]
    d = {}
    first = True
    for i, item in enumerate(l):
        if first:
            first = False
        else:
            ilen = len(item.split())
            if i != len(l) - 1:
                val = " ".join(item.split()[0:ilen - 1])
                d[key.strip(" ")] = val
                key = item.split()[-1]
            else:
                val = item
                d[key.strip(" ")] = val
    return d

'''''
false
def listToDict(o, ksep, sep):
    od = {}
    key = "delete"
    value = ""
    for i in o.split(sep):
        if ":" in i:
            if i.endswith(ksep):
                od[key] = value
                key = i.strip(ksep)
                value = ""
            else:
                k,v = i.split(ksep)
                key = k
                value = v
        else:
            value += " " + i
    del od["delete"]
    return od
'''''

def hasError(s):
    # chk = s.lower()
    for x in errormsgs:
        if x in s:
            return True
    return False

def validVuln(s):
    vals = ["VULNERABLE:"]
    for val in vals:
        if val not in s:
            return False
    return True

def sanitize(st):
    return st.replace('\n', '').replace('\t','').replace('"', '')


'''''
s =  "VULNERABLE:  SMBv2 exploit (CVE-2009-3103, Microsoft Security Advisory 975497)    State: VULNERABLE    IDs:  CVE:CVE-2009-3103          Array index error in the SMBv2 protocol implementation in srv2.sys in Microsoft Windows Vista Gold, SP1, and SP2,          Windows Server 2008 Gold and SP2, and Windows 7 RC allows remote attackers to execute arbitrary code or cause a          denial of service (system crash) via an & (ampersand) character in a Process ID High header field in a NEGOTIATE          PROTOCOL REQUEST packet, which triggers an attempted dereference of an out-of-bounds memory location,          aka SMBv2 Negotiation Vulnerability.              Disclosure date: 2009-09-08    References:      https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2009-3103      http://www.cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2009-3103"

s2 = "CVE:CVE-2009-3103 Array index error in the SMBv2 protocol implementation in srv2.sys in Microsoft Windows Vista Gold, SP1, and SP2, Windows Server 2008 Gold and SP2, and Windows 7 RC allows remote attackers to execute arbitrary code or cause a denial of service (system crash) via an & (ampersand) character in a Process ID High header field in a NEGOTIATE PROTOCOL REQUEST packet, which triggers an attempted dereference of an out-of-bounds memory location, aka SMBv2 Negotiation Vulnerability. Disclosure"

wl = s2.split()
cve = wl[0]
desc = " ".join(wl[1:])
# s = sanitize(s)
'''''