#!/usr/bin/env python
import pprint

from canari.maltego.utils import debug, progress
from canari.framework import configure #, superuser
from common.coreutil import sanitize

from common.nmaputil import getParsedReport, doSmbVuln

from common.entities import Port, OHost

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, Oscp Project'
__credits__ = []

__license__ = 'GPL'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

__all__ = [
    'dotransform',
    'onterminate' # comment out this line if you don't need this function.
]


"""
TODO: set the appropriate configuration parameters for your transform.
TODO: Uncomment the line below if the transform needs to run as super-user
"""
#@superuser
@configure(
    label='SMB Vulnernabilities',
    description='Enumerates the SMB Vulns from Nmap File',
    uuids=[ 'TODO something.v2.SomethingToPhrase_HelloWorld' ],
    inputs=[ ( 'oscp', OHost ) ],
    debug=True
)
def dotransform(request, response, config):
    """
    Check SMB Vulnerabilities
    """
    ip = request.value
    parsedreport = getParsedReport("/mnt/64G/proj/oscp-maltego/nmapsmbvuln.xml")
    for _host in parsedreport.hosts:
        if _host.address == ip:
            scripts = _host.scripts_results
            for res in scripts:
                if "smb-vuln" in res.get('id'):
                    v = doSmbVuln(sanitize(res.get('output')))
                    if v is not None:
                        response += v
    return response

def onterminate():
    """
    TODO: Write your cleanup logic below or delete the onterminate function and remove it from the __all__ variable
    """
    pass