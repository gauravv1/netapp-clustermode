import sys
from NaServer import *
import json



_create_unverified_https_context = ssl._create_unverified_context
ssl._create_default_https_context = _create_unverified_https_context

usage = """
Usage: ./volume-list.py filername or IP
e.g. ./volume-list.py filer1
"""

if len(sys.argv)!=2:
    print (usage)
    sys.exit(0)

filer_name = sys.argv[1]

s = NaServer(filer_name, 1 , 20)
s.set_server_type("FILER")
s.set_transport_type("HTTPS")
s.set_port(443)
s.set_style("LOGIN")
s.set_admin_user("admin", "password123")

def readable_size(size):
    for unit in ['bytes','KB','MB','GB','TB']:
        if size < 1000.0 and size > -1000.0:
            return "%3.2f %s" % (size, unit)
        size /= 1000.0
    return "%3.2f %s" % (size, 'PB')

cmd = NaElement('volume-get-iter')
cmd.child_add_string('max-records', '200')

out = s.invoke_elem(cmd)

if(out.results_status() == "failed"):
        print "%s failed." % filer_name
        print(out.results_reason() + "\n")
        sys.exit(2)

if(out.child_get_int("num-records") == "0"):
        print "%s failed." % filer_name
        print "no volumes found.\n"
        sys.exit(2)

print '\n%s : Volume Report : \n' % filer_name

vollist = dict()
vollist = out.child_get('attributes-list')

print "Vserver      Volume      Aggregate   Type    State    Total size    Available size"
for volattr in vollist.children_get():
	volstateattrs = dict()
	volstateattrs = volattr.child_get('volume-state-attributes')
for volstateattr in vollist.children_get():
	volsizeattrs = dict()
	volsizeattrs = volstateattr.child_get('volume-space-attributes')
for vol in vollist.children_get():
	volattrs = dict()
	volattrs = vol.child_get('volume-id-attributes')
	print volattrs.child_get_string('owning-vserver-name'),
	print volattrs.child_get_string('name'),
	print volattrs.child_get_string('containing-aggregate-name'),
	print volattrs.child_get_string('type'),
	print volstateattrs.child_get_string('state'),
	print readable_size(int(volsizeattrs.child_get_string('size'))),
	print readable_size(int(volsizeattrs.child_get_string('size-available')))
print '---------------------------------'
