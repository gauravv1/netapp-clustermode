######Snapmirror status for broken relations in 7 mode. 

#!/usr/bin/python
import xmltodict
import json
import sys
from NaServer import *

filer_name = sys.argv[1]
s = NaServer(filer_name, 1 , 19)
s.set_server_type("FILER")
s.set_transport_type("HTTPS")
s.set_port(443)
s.set_style("LOGIN")
s.set_admin_user("root", "password123")


api = NaElement("snapmirror-get-status")

xo = s.invoke_elem(api)

obj = xmltodict.parse(xo.sprintf())
jd = json.dumps(obj)
jl = json.loads(jd)

if xo.results_status() == "failed":
        reason = xo.results_reason()
        print ("Failure: %s" %reason)
else:
        for h in jl["results"]["snapmirror-status"]["snapmirror-status-info"]:
                if h["state"] == "broken-off":

                        print h["source-location"],
                        print h["destination-location"],
                        print h["status"],
                        print h["state"],
                        m, s = divmod(int(h["lag-time"]), 60)
                        h, m = divmod(m, 60)
                        print "%d:%02d:%02d" % (h, m, s)
                else:
                        pass
