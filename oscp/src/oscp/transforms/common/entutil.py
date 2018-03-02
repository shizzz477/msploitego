import pprint

from entities import Port, Vulnerability


def toPort(mobj):
    pn = mobj.getVar('oscp.portnumber')
    op = Port(pn)
    op.protocol = mobj.getVar('oscp.protocol')
    # mobj.debug("Protocol: " + op.protocol)
    op.source = mobj.getVar('ip.source')
    # mobj.debug("IP: " + op.source)
    op.portnumber = mobj.getVar('oscp.portnumber')
    # mobj.debug("Port: " + op.portnumber)
    op.servicename = mobj.getVar('oscp.servicename')
    # mobj.debug("Service: " + op.servicename)
    return op

'''''
vulnerable', displayname='Vulnerable', value=True
vulnstate', displayname='Vulnerabilty State'
vulndescription', displayname='Description'
vulnref', displayname='References'
vulnids', displayname='IDs'
'''''
def createVulnerability(dict):
    v = Vulnerability(dict['VULNERABLE'])
    vfields = dir(v)
    inputfields = dict.keys()
    for f in inputfields:
        if "__" in f:
            continue
        if f in vfields:
            setattr(v, f, dict[f])
    return v

'''''
    v.vulnerable = dict['VULNERABLE']
    v.vulnstate = dict['State']
    iddesc = dict['IDs']
    # TODO: what if multiple IDs
    if iddesc is not None:
        wl = iddesc.split()
        v.vulnids = wl[0]
        v.vulndescription = " ".join(wl[1:])
    v.disclosuredate = dict['date']
    v.vulnref = dict['References']
'''''


# noinspection PyUnreachableCode
'''''
op = Port("139")
op.portnumber = "139"
op.servicename = "netbios"
op.protocol = "tcp"
op.source = "10.11.1.5"
op.state = "open"
print str(dir(op))
setattr(op, "protocol", 'magic')
pprint.pprint(op)
'''''