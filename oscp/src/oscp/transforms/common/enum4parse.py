#!/usr/bin/env python
import pprint

from coreutil import sanitize

inf = {}
def enum4parser(filename):
    chunk = {}
    with open(filename, 'r') as file:
        line = next(file)
        while line:
            # get top banner
            while "=========" not in line:
                line = next(file)
            line = next(file)
            if line:
                b = line.replace('|', '').replace(' ', '')
                if "Gettingprinter" in b:
                    break
            # throw out bottom banner
            line = next(file)
            line = next(file)
            # store all until next banner
            val = []
            while "=========" not in line:
                line = next(file).replace('\n', '').replace('\t','').replace('"', '')
                if line and "==========" not in line and "[V]" not in line:
                    val.append(line)
            chunk[b] = val
    return chunk

def doWorkgroup(d):
    global inf
    wgroups = []
    for l in d:
        if '[+]' in l:
            if "Got domain" in l:
                line = l.split()
                wgroups.append(line[-1])
    inf['workgroups'] = wgroups

def doDomainSID(d):
    global inf
    skipwords = [
        'part of a workgroup'
    ]
    dsid = {}
    for l in d:
        if any(x in l for x in skipwords):
            pass
        if "Domain Name" in l:
            ln = l.split()
            dsid['domain'] = ln[-1]
        elif "Domain Sid" in l:
            ln = l.split()
            dsid['sid'] = " ".join(ln[2:])
        elif '[+]' in l:
            dsid['comment'] = l.replace('\\\\','')
        else:
            pass
    if dsid:
        inf['domainsid'] = dsid

def getNext(i, d):
    lst = []
    i += 1
    l = d[i]
    while "[+]" not in l and not None:
        lst.append(l.split(":")[1].split("]")[0].strip("["))
        i += 1
        l = d[i]
    return lst, i

def skiplines(i, d):
    length = len(d)
    i += 1
    l = d[i]
    while "[+]" not in l and not None:
        i += 1
        if i >= len(d) - 1:
            return None
        else:
            l = d[i]
    return i

def doGroups(d):
    global inf
    groups = {}
    bgroups = []
    lgroups = []
    dgroups = []
    i = 0
    while i < len(d) - 1:
        l = d[i]
        if "[+] Getting builtin groups" in l:
            bgroups, i = getNext(i, d)
            l = d[i]
        elif "[+] Getting local groups" in l:
            lgroups, i = getNext(i, d)
            l = d[i]
        elif "[+] Getting domain groups" in l:
            dgroups, i = getNext(i, d)
            l = d[i]
        else:
            # print "*** not processsing, " + l + " ***"
            i = skiplines(i, d)
            if i is None:
                break
            else:
                l = d[i]
    if bgroups:
        groups['builtin'] = bgroups
    if dgroups:
        groups['domain'] = dgroups
    if lgroups:
        groups['local'] = lgroups
    if groups:
        inf['groups'] = groups

def doNbStat(d):
    global inf
    nb = {}
    for l in d:
        if "MAC Address" in l:
            pass
        else:
            val = l.split()[0]
            k = l.split()[5:]
            nb[" ".join(k).strip('<ACVTIVE>').replace(' ','')] = val
    if nb:
        inf['nbtstat'] = nb

def doOsInfo(d):
    global inf
    i = 0
    skipwords = [
        'NT_STATUS_INVALID',
        '[V]'
    ]
    osinfo = {}
    smbclientinfo = []
    srvinfo = {}
    l = d[i]
    while i < len(d) - 1:
        if any(x in l for x in skipwords):
            i += 1
            l = d[i]
        elif "from smbclient" in l:
            i += 1
            l = d[i]
            while "[+]" not in l:
                if any(x in l for x in skipwords):
                    i += 1
                    l = d[i]
                else:
                    smbclientinfo.append(l)
                    i += 1
                    l = d[i]
            if smbclientinfo:
                osinfo['smbclientinfo'] = smbclientinfo
        elif "from srvinfo" in l:
            i += 1
            l = d[i]
            while "[+]" not in l:
                if any(x in l for x in skipwords):
                    i += 1
                    if i >= len(d):
                        break
                    else:
                        l = d[i]
                else:
                    key = l.split()[0]
                    val = " ".join(l.split()[1:])
                    srvinfo[key] = val
                    i += 1
                    if i >= len(d):
                        break
                    else:
                        l = d[i]
            if srvinfo:
                osinfo['srvinfo'] = srvinfo
    if osinfo:
        inf['osinfo'] = osinfo

def doShares(d):
    global inf
    shares = {}
    skipwords = [
        'WARNING',
        'Comment',
        '---------',
        'Reconnecting',
        'Workgroup',
        'ACCESS_DENIED'
    ]
    i = 0
    l = d[i]
    while i < len(d):
        if "[+] Attempting to map shares" in l:
            break
        elif any(x in l for x in skipwords):
            i += 1
            l = d[i]
        else:
            key = l.split()[0]
            value = " ".join(l.split()[1:])
            shares[key] = value
            i += 1
            l = d[i]
    if shares:
        inf['shares'] = shares

def doUsers(d):
    global inf
    users = {}
    skipwords = [
        'index: 0x',
        'user:['
    ]
    i = 0
    l = d[i]
    while i < len(d):
        if "ZZZZZZZZZZZZZZZZZ" in l:
            break
        elif any(x in l for x in skipwords):
            i += 1
            l = d[i]
        elif "User Name" in l:
            user = {}
            # key = l.split(':')[0].strip().replace(' ','')
            username = " ".join(l.split(':')[1:])
            i += 1
            l = d[i]
            while "User Name" not in l:
                key = l.split(':')[0].strip().replace(' ', '')
                val = " ".join(l.split(':')[1:])
                if val:
                    user[key] = val
                i += 1
                if i >= len(d):
                    break
                else:
                    l = d[i]
            if user:
                users[username] = user
    if users:
        inf['users'] = users

def getEnum4(ip):
    filename = "/root/data/oscp_prep/repo/enum4/" + ip + "-enum4.txt"
    chunks = enum4parser(filename)

    for k, data in chunks.iteritems():
        if "EnumeratingWorkgroup" in k:
            if data:
                doWorkgroup(data)
        elif "GettingdomainSID" in k:
            if data:
                doDomainSID(data)
        elif "Groupson" in k:
            if data:
                doGroups(data)
        elif "MachineEnumerationon" in k:
            pass
        elif "NbtstatInformation" in k:
            if data:
                doNbStat(data)
        elif "OSinformationon" in k:
            if data:
                doOsInfo(data)
        elif "PasswordPolicyInformation" in k:
            pass
        elif "SessionCheck" in k:
            if data:
                sessions = []
                for l in data:
                    sessions.append(l)
                inf['sessioncheck'] = sessions
        elif "ShareEnumeration" in k:
            if data:
                doShares(data)
        elif "viaRIDcycling" in k:
            pass
        elif "Userson" in k:
            if data:
                doUsers(data)
        elif "TargetInformation" in k:
            pass
        else:
            pass
            # print "**** key not found " + k
    return inf

data = getEnum4("10.11.1.31")
pprint.pprint(data)
'''''
chunks = {}
while True:
    l = getLine()
    if "=========" in l:
        # top banner line
        next = getLine()    # banner
        b = next.replace('|','').replace(' ', '')
        print b
        next = getLine()    # skip lower banner
        next = getLine()
        val = ""
        while "=========" not in next:
            val += next
            next = getLine()
        chunks[b] = val
        pprint.pprint(chunks)
        
        
               elif "[+] Getting builtin group memberships" in l:
            print "*** not processsing, Getting builtin group memberships check file ***"
            dummy, i = getNext(i, d)
            print i
            l = d[i]
        elif "[+] Getting detailed info for group" in l:
            print "*** not processsing, Getting detailed info for group check file ***"
            dummy, i = getNext(i, d)
            print i
            l = d[i]
        elif "[+] Getting local group memberships" or "[+] Getting domain group memberships" in l:
            print "*** not processsing, Getting local group memberships check file ***"
            dummy, i = getNext(i, d)
            print i
            l = d[i]
            elif "[+] Getting local groups":
            l = getNext(i, d)
            if l is None:
                break
            else:
                i += 1
            while "[+]" not in l:
                g = l.split(":")[1].split("]")[0].strip("[")
                if g:
                    lgroups.append(g)
                l = getNext(i, d)
                if l is None:
                    break
                else:
                    i += 1
'''''