import sys
from NaServer import *
import xmltodict
import json


filer_name = sys.argv[1]

filer = NaServer(filer_name,1,6)
filer.set_admin_user("admin","$wgdw1c!")
cmd = NaElement("perf-object-get-instances")
cmd1 = NaElement("net-port-get-iter")
port = filer.invoke_elem(cmd1)


obj = xmltodict.parse(port.sprintf())
jdump = json.dumps(obj)
jload = json.loads(jdump)


xi = NaElement("counters")
cmd.child_add(xi)
xi.child_add_string("counter","rx_total_errors")
xi2 = NaElement("instances")
cmd.child_add(xi2)

for h in jload['results']['attributes-list']['net-port-info']:
        if h['port-type'] == 'physical':
                xi2.child_add_string("instance",h['port'])
                cmd.child_add_string("objectname","nic_common")
                err = filer.invoke_elem(cmd)
                a = xmltodict.parse(err.sprintf())
                jd = json.dumps(a)
                jl = json.loads(jd)
                for x in jl['results']['instances']['instance-data']:
                        n = int(x['counters']['counter-data']['value'])
                        if n > 1000:
                                print x['uuid'],
                                print x['counters']['counter-data']['value']
                        else:
                                pass
