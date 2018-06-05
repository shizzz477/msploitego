from pprint import pprint

from datetime import datetime

from common.MaltegoTransform import *
from common.postgresdb import MsploitPostgres
import sys

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
    sessionid = mt.getValue()
    mpost = MsploitPostgres("msf", "unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE=", "msf")
    for detail in mpost.getSessionDetails(sessionid):
        detailent = mt.addEntity("msploitego.SessionDetail", str(detail.get("id")))
        detailent.setValue(str(detail.get("id")))
        for k,v in detail.items():
            if isinstance(v,datetime):
                detailent.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                detailent.addAdditionalFields(k, k.capitalize(), False, str(v))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['sessiondetails.py',
#  '37',
#  'properties.meterpretersession=37#close_reason=Died#via_payload=payload/windows/meterpreter/bind_tcp#via_exploit=exploit/windows/dcerpc/ms03_026_dcom#port=135#platform=x86/windows#local_id=1#opened_at=31/5/2018#address=10.11.1.5#host_id=517#datastore=BAh7OSINRVhJVEZVTkMiC3RocmVhZCIOV09SS1NQQUNFSSIABjoGRUYiDFZF\nUkJPU0VJIgl0cnVlBjsARiINV2ZzRGVsYXlJIgYwBjsARiIaRW5hYmxlQ29u\ndGV4dEVuY29kaW5nSSIKZmFsc2UGOwBGIhtDb250ZXh0SW5mb3JtYXRpb25G\naWxlSSIABjsARiIaRGlzYWJsZVBheWxvYWRIYW5kbGVySSIKZmFsc2UGOwBG\nSSIKUkhPU1QGOwBGIg4xMC4xMS4xLjVJIgpSUE9SVAY7AEZJIggxMzUGOwBG\nIghTU0xJIgpmYWxzZQY7AEYiD1NTTFZlcnNpb24iCUF1dG8iElNTTFZlcmlm\neU1vZGUiCVBFRVIiDlNTTENpcGhlckkiAAY7AEZJIgxQcm94aWVzBjsARkki\nAAY7AEZJIgpDUE9SVAY7AEZJIgAGOwBGSSIKQ0hPU1QGOwBGSSIABjsARiIT\nQ29ubmVjdFRpbWVvdXRJIgcxMAY7AEYiF1RDUDo6bWF4X3NlbmRfc2l6ZUki\nBjAGOwBGIhRUQ1A6OnNlbmRfZGVsYXlJIgYwBjsARiIaRENFUlBDOjptYXhf\nZnJhZ19zaXplSSIJNDA5NgY7AEYiHERDRVJQQzo6ZmFrZV9iaW5kX211bHRp\nSSIJdHJ1ZQY7AEYiJERDRVJQQzo6ZmFrZV9iaW5kX211bHRpX3ByZXBlbmRJ\nIgYwBjsARiIjRENFUlBDOjpmYWtlX2JpbmRfbXVsdGlfYXBwZW5kSSIGMAY7\nAEYiF0RDRVJQQzo6c21iX3BpcGVpbyIHcnciGERDRVJQQzo6UmVhZFRpbWVv\ndXRJIgcxMAY7AEYiC1RBUkdFVEkiBjAGOwBGIgxQQVlMT0FEIiF3aW5kb3dz\nL21ldGVycHJldGVyL2JpbmRfdGNwIgpMSE9TVCIQMTAuMTEuMC4xMDEiCkxQ\nT1JUSSIKMjEyODEGOwBGSSIUUGF5bG9hZFVVSURTZWVkBjsAVEkiAAY7AEZJ\nIhNQYXlsb2FkVVVJRFJhdwY7AFRJIgAGOwBGSSIUUGF5bG9hZFVVSUROYW1l\nBjsAVEkiAAY7AEZJIhhQYXlsb2FkVVVJRFRyYWNraW5nBjsAVEkiCmZhbHNl\nBjsARiIYRW5hYmxlU3RhZ2VFbmNvZGluZ0kiCmZhbHNlBjsARiIRU3RhZ2VF\nbmNvZGVySSIABjsARiIeU3RhZ2VFbmNvZGVyU2F2ZVJlZ2lzdGVycyIAIhpT\ndGFnZUVuY29kaW5nRmFsbGJhY2tJIgl0cnVlBjsARiITUHJlcGVuZE1pZ3Jh\ndGVJIgpmYWxzZQY7AEYiF1ByZXBlbmRNaWdyYXRlUHJvY0kiAAY7AEYiE0F1\ndG9Mb2FkU3RkYXBpSSIJdHJ1ZQY7AEYiFkF1dG9WZXJpZnlTZXNzaW9uSSIJ\ndHJ1ZQY7AEYiHUF1dG9WZXJpZnlTZXNzaW9uVGltZW91dEkiBzMwBjsARiIZ\nSW5pdGlhbEF1dG9SdW5TY3JpcHQiACISQXV0b1J1blNjcmlwdCIAIhNBdXRv\nU3lzdGVtSW5mb0kiCXRydWUGOwBGIhpFbmFibGVVbmljb2RlRW5jb2RpbmdJ\nIgpmYWxzZQY7AEYiE0hhbmRsZXJTU0xDZXJ0SSIABjsARiIWU2Vzc2lvblJl\ndHJ5VG90YWxJIgkzNjAwBjsARiIVU2Vzc2lvblJldHJ5V2FpdEkiBzEwBjsA\nRiIdU2Vzc2lvbkV4cGlyYXRpb25UaW1lb3V0SSILNjA0ODAwBjsARiIgU2Vz\nc2lvbkNvbW11bmljYXRpb25UaW1lb3V0SSIIMzAwBjsARiIeUGF5bG9hZFBy\nb2Nlc3NDb21tYW5kTGluZSIA\n#last_seen=31/5/2018#closed_at=31/5/2018#id=37#stype=meterpreter']
#
# dotransform(args)