import sys
from NaServer import *
import xmltodict
import json

_create_unverified_https_context = ssl._create_unverified_context
ssl._create_default_https_context = _create_unverified_https_context


filer_name = sys.argv[1]

filer = NaServer(filer_name,1,6)
filer.set_admin_user("admin", "password123")
cmd = NaElement("fcp-adapter-stats-get-iter")
ret = filer.invoke_elem(cmd)



obj = xmltodict.parse(ret.sprintf())
jdump = json.dumps(obj)
jload = json.loads(jdump)

print "Node           Port             Errors"

for h in jload['results']['attributes-list']['fcp-adapter-stats-info']:
        print h['node'],
        print h['adapter'],
        print h['crc-errors']
