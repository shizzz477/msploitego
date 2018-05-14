import re
from pprint import pprint
from common.nsescriptlib import cleanresults, scriptrunner
from common.MaltegoTransform import *
import sys

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

nmap_proc = None

def mycallback(nmaptask):
    nmaptask = nmap_proc.current_task
    if nmaptask:
        print "Task {0} ({1}): ETC: {2} DONE: {3}%".format(nmaptask.name,
                                                              nmaptask.status,
                                                              nmaptask.etc,
                                                              nmaptask.progress)
def listgen(l):
    for i in l:
        yield i

# def uniqcomment(t,l):
#     for d in l:
#         if d.get("Comment") == t:
#             return False
#     return True

def cleanoutput(d):
    lgen = listgen(d.get("output").split("\n"))
    comment = {}
    comments = []
    for line in lgen:
        a1 = line.strip()
        if a1:
            a2 = a1.split(":")
            tag = a2[0]
            data = ":".join(a2[1::])
            if tag.lower() == "comment":
                while tag != "Path":
                    try:
                        t = lgen.next().lstrip()
                        t1 = t.split(":")
                        if t1[0] == "Path":
                            comment.update({"Comment": data})
                            tag = "Path"
                            data = ":".join(t1[1::])
                            break
                        data += t
                    except StopIteration:
                        comments.append(comment)
                        break
            if comment and tag.lower() == "path":
                comments.append(comment)
                comment = {}
            comment.update({tag:data})
    # b = [a.replace("'", "").replace("/", "").lstrip("\n").lstrip(" ").split("\n")][0]
    # c = [x for x in b if ":" in x]
    return comments

def dotransform(args):
    global nmap_proc
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")

    rep = scriptrunner(port,"http-comments-displayer", ip)
    for scriptrun in rep.hosts[0].services[0].scripts_results:
        comments = cleanoutput(scriptrun)

        for comment in comments:
           if "Comment" in comment:
               c = comment.get("Comment")
               if re.search('[a-zA-Z]', c):
                   commententity = mt.addEntity("msploitego.SourceCodeComment", c)
                   commententity.setValue(c)
                   commententity.addAdditionalFields("comment", "Comment", False, c)
                   commententity.addAdditionalFields("path", "Path", False, comment.get("Path"))
               # commententity.addAdditionalFields("linenumber", "Line Number", False, comment.get("Line Number"))

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['httpcomments.py',
#  'http/80:249',
#  'properties.metasploitservice=http/80:249#info=Microsoft IIS httpd 10.0#name=http#proto=tcp#hostid=249#service.name=80/Apache 9#port=80#banner=Apache 9#properties.service= #ip=10.10.10.80#fromfile=/root/proj/oscp-maltego/oscp/src/oscp/transforms/common/msploitdb20180501.xml#state=open']
# dotransform(args)

# {'output': "\n  /css/: Potentially interesting directory w/ listing on 'apache/2.4.25 (ubuntu)'\n  /images/: Potentially interesting directory w/ listing on 'apache/2.4.25 (ubuntu)'\n  /js/: Potentially interesting directory w/ listing on 'apache/2.4.25 (ubuntu)'\n  /uploads/: Potentially interesting folder\n", 'elements': {}, 'id': 'http-enum'}