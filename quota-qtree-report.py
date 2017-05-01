import sys
from NaServer import *
import xmltodict
import json

_create_unverified_https_context = ssl._create_unverified_context
ssl._create_default_https_context = _create_unverified_https_context

class Set_filer:
		
	def a(self, api, filer_name):
		s = NaServer(filer_name, 1 , 20)
		s.set_server_type("FILER")
		s.set_transport_type("HTTPS")
		s.set_port(443)
		s.set_style("LOGIN")
		s.set_admin_user("admin", "password123")
		a = s.invoke_elem(api)
		out = a.sprintf()
		return out

def qtree():
	filer_name = raw_input("Enter Cluster name or IP:")
	api = NaElement("qtree-list-iter")
	m = Set_filer()
	out =  m.a(api, filer_name)

	obj = xmltodict.parse(out)
	jdump = json.dumps(obj)
	final = json.loads(jdump)
	
	print "Vserver   Policy   Volume   Qtree"
	print "---------------------------------"
	for h in  final['results']['attributes-list']['qtree-info']:
		print h['vserver'],
		print h['export-policy'],
		print h['volume'],
		print h['qtree']


def quota():
	
	filer_name = raw_input("Enter Cluster name or IP:")
        api = NaElement("quota-list-entries-iter")
        m = Set_filer()
        out =  m.a(api, filer_name)
	obj = xmltodict.parse(out)
        jdump = json.dumps(obj)
        final = json.loads(jdump)
	print "Vserver	Quota-Type	Disk-Limit	Qtree"
	print "----------------------------------------------"
	for h in  final['results']['attributes-list']['quota-entry']:
		print h['vserver'],
		print h['quota-type'],
		print h['disk-limit'],
		print h['quota-target']
		

############Qtree Menu#####################3

print """
        Enter 1 to see qtree report
        Enter 2 to see quota report
"""
choice = int(raw_input("Enter choice:"))


if choice == 1:
	qtree()

elif choice == 2:
	quota()
else:
	print ("Please enter correct choice. Good Bye!")
