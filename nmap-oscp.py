#!/usr/bin/env python
#
# NMAP OSCP Scanner
# Written by Marc Silver (@bsdkid)
# marcs@bsdkid.com
#
# The aim of this script was to make enumeration and searching in the
# OSCP lab a little easier, particularly when wanting different scan
# results or the ability to search through results.
#
# This software comes with no disclaimer or warranty.  You may use it
# and modify it as you wish but please provide credit to the original
# author.
#
# #

import re
import os
import sys
import nmap
import glob
import argparse

# Change this to your preferred output directory.
outputdir = '/root/scan-results'

try:
    nm = nmap.PortScanner()
except:
    print 'Unable to find nmap, exiting.'
    sys.exit()

if not os.path.exists(outputdir) or not os.path.isdir(outputdir):
    print 'Output directory ({0}) does not exist, please create.'.format(outputdir)
    sys.exit()

# Define hosts for later use
hosts = {}

def search_results(DATA, scanAll, ip, port):
    if scanAll is True:
        SCOPE = DATA
    else:
        SCOPE = {}
        SCOPE[ip] = DATA[ip]

    for host in SCOPE:
        nm.analyse_nmap_xml_scan(DATA[host])
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                lport = list(nm[host][proto].keys())
                lport.sort()
                for seenport in lport:
                    if int(seenport) == int(port):
                        print '{0} : {1}/{2} ({3})'.format(host, proto, port, nm[host][proto][seenport]['state'])

def view_output(DATA, scanAll, ip):
    if scanAll is True:
        SCOPE = DATA
    else:
        SCOPE = {}
        SCOPE[ip] = DATA[ip]

    for host in SCOPE:
        nm.analyse_nmap_xml_scan(DATA[host])
        for address in nm.all_hosts():
            print '\nHost: {0} ({1})'.format(address, nm[address].hostname())
            print '  State: {0}'.format(nm[address].state())
            for proto in nm[address].all_protocols():
                print '  Protocol: {0}'.format(proto)
                lport = list(nm[address][proto].keys())
                lport.sort()
                for port in lport:
                    print '    {0} ({1})'.format(port, nm[address][proto][port]['state'])

def get_data():
    for file in glob.glob(outputdir + '/*.xml'):
        with open(file, 'r') as fd:
            content = fd.read()
            nm.analyse_nmap_xml_scan(content)
            for host in nm.all_hosts():
                if host not in hosts:
                    hosts[host] = content
    return hosts

def nmap_scan(ip, scantype):
    try:
        print 'Running a {0} scan against {1}'.format(scantype, ip)
        if scantype == 'quick':
            scanArgs = None
        elif scantype == 'udp':
            scanArgs = '-O -Pn -sU -p-'
        elif scantype == 'tcp':
            scanArgs = '-O -Pn -sT -p-'
        elif scantype == 'info':
            scanArgs = '-O -A'
        elif scantype == 'full':
            scanArgs = '-O -Pn -sTU -p-'
        if scanArgs is None:
            nm.scan(ip)
        else:
            nm.scan(ip, arguments=scanArgs)
        return nm
    except:
        print 'Unable to run nmap scan.'

def write_output_file(ip, scantype, result):
    #ip = ip.replace("/", "-")
    filename = outputdir + '/' + ip + '-' + scantype + '.xml'
    try:
        outputfile = open(filename, 'w')
        outputfile.truncate()
        outputfile.write(result)
        outputfile.close()
    except:
        print 'Unable to write output ({0}) to disk.'.format(filename)

def main():
    DATA = get_data()
    if args.a:
        scanAll = True
    else:
        scanAll = False
    if args.view:
        view_output(DATA, scanAll, args.ip)
    if args.scan:
        nm = nmap_scan(args.ip, args.scan)
        write_output_file(args.ip, args.scan, nm.get_nmap_last_output())
    if args.port:
        print 'Looking for port {0}...'.format(args.port)
        search_results(DATA, scanAll, args.ip, args.port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'Enumerate a host or list of hosts',
        epilog='NOTE: new scans will overwrite previous scan data.'
    )
    parser.add_argument('-ip', help='IP address of host')
    parser.add_argument('-port', help='Run a search for a port')
    parser.add_argument('-scan', help='Run specified scan', choices=['quick', 'full', 'info', 'tcp', 'udp'])
    parser.add_argument('-view', help='View scan data', action='store_true')
    parser.add_argument('-a', help='(SEARCH ONLY): Run a search against files in the output dir', action='store_true')
    args = parser.parse_args()
    if (not args.ip and not args.a) or (args.ip and args.a):
        parser.print_help()
    else:
        main()
