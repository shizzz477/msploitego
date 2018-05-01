#!/usr/bin/env python

import xml.etree.ElementTree as ET
from pprint import pprint

root = ET.parse("/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/msploitdb20180430.xml").getroot()

#for node in root.iter("module_details"):
root.remove(root.find("module_details"))
# root.remove(node)
print "removed"