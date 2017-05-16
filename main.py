#/usr/bin/python
import xmltodict
import json
import sys
from NaServer import *

filer_name = sys.argv[1]

s = NaServer(filer_name, 1 , 32)
s.set_server_type("FILER")
s.set_transport_type("HTTPS")
s.set_port(443)
s.set_style("LOGIN")
s.set_admin_user("admin", "$wgdw1c!")


def cluster_info(s):
        api = NaElement("cluster-identity-get")

        xi = NaElement("desired-attributes")
        api.child_add(xi)


        xi1 = NaElement("cluster-identity-info")
        xi.child_add(xi1)

        xi1.child_add_string("cluster-contact","<cluster-contact>")
        xi1.child_add_string("cluster-location","<cluster-location>")
        xi1.child_add_string("cluster-name","<cluster-name>")
        xi1.child_add_string("cluster-serial-number","<cluster-serial-number>")

        xo = s.invoke_elem(api)

        if xo.results_status() == "failed":
                reason = xo.results_reason()
                print ("Failure: %s" %reason)
        else:

                obj = xmltodict.parse(xo.sprintf())
                jdump = json.dumps(obj)
                jload = json.loads(jdump)
                print "Cluster Location     Name        Serial#"
                print "========================================"
                print jload["results"]["attributes"]["cluster-identity-info"]["cluster-location"],
                print ("   %s      " % jload["results"]["attributes"]["cluster-identity-info"]["cluster-name"]),
                print jload["results"]["attributes"]["cluster-identity-info"]["cluster-serial-number"]



def alarm(s):

        api = NaElement("dashboard-alarm-get-iter")
        api.child_add_string("max-records","100")

        xi = NaElement("query")
        api.child_add(xi)

        xi.child_add_string("dashboard-alarm-info","<dashboard-alarm-info>")

        xo = s.invoke_elem(api)


        obj = xmltodict.parse(xo.sprintf())
        jd = json.dumps(obj)
        jl = json.loads(jd)

        if xo.results_status() == "failed":
                reason = xo.results_reason()
                print ("Failure: %s" %reason)
        else:
                if xo.child_get_int('num-records') == 0:
                        pass
                else:

                        xo1=xo.child_get("attributes-list")
                        metric = xo1.child_get("dashboard-alarm-info").child_get_string("dashboard-metric-type")
                        node = xo1.child_get("dashboard-alarm-info").child_get_string("node")
                        obj = xo1.child_get("dashboard-alarm-info").child_get_string("object-name")
                        state = xo1.child_get("dashboard-alarm-info").child_get_string("state")

                        print "Node          Alert        State    Object"
                        print "================================================="


                        print node,
                        print metric,
                        print state,
                        print obj

def aggr(s):
        api = NaElement("aggr-get-iter")
        api.child_add_string("max-records","100")

        xi = NaElement("query")
        api.child_add(xi)

        xi.child_add_string("aggr-attributes","<aggr-attributes>")

        xo = s.invoke_elem(api)

        obj = xmltodict.parse(xo.sprintf())
        jd = json.dumps(obj)
        jl = json.loads(jd)

        print "Node             Aggr            State"
        print "======================================"

        if xo.results_status() == "failed":
                reason = xo.results_reason()
                print ("Failure: %s" %reason)
        else:

                for h in jl["results"]["attributes-list"]["aggr-attributes"]:
                        state = h["aggr-raid-attributes"]["state"]
                        if state != 'online':

                                print h["nodes"]["node-name"],
                                print h["aggregate-name"],
                                print h["aggr-raid-attributes"]["state"]
                        else:
                                print "No offline aggregate."
                                break

def vol(s):
        api = NaElement("volume-get-iter")
        api.child_add_string("max-records","1000")

        xi = NaElement("query")
        api.child_add(xi)

        xi.child_add_string("volume-attributes","<volume-attributes>")

        xo = s.invoke_elem(api)


        obj = xmltodict.parse(xo.sprintf())
        jd = json.dumps(obj)
        jl = json.loads(jd)


        print "Vserver                  Volume                   State"
        print "======================================================="

        if xo.results_status() == "failed":
                reason = xo.results_reason()
                print ("Failure: %s" %reason)
        else:
                for h in jl["results"]["attributes-list"]["volume-attributes"]:
                        if h["volume-state-attributes"]["state"] != 'online':

                                print h["volume-id-attributes"]["owning-vserver-name"],
                                print h["volume-id-attributes"]["name"],
                                print h["volume-state-attributes"]["state"]
                        else:
                                print "No offline volume"
                                break


def sensors(s):
        api = NaElement("environment-sensors-get-iter")
        api.child_add_string("max-records","1000")

        xi = NaElement("query")
        api.child_add(xi)

        xi.child_add_string("environment-sensors-info","<environment-sensors-info>")

        xo = s.invoke_elem(api)

        obj = xmltodict.parse(xo.sprintf())
        jd = json.dumps(obj)
        jl = json.loads(jd)

        print "Node             Sensor          Status"
        print "======================================="
        if xo.results_status() == "failed":
                reason = xo.results_reason()
                print ("Failure: %s" %reason)
        else:


                for h in jl["results"]["attributes-list"]["environment-sensors-info"]:

                        if "Fan" in h["sensor-name"]:
                                print h["node-name"],
                                print h["sensor-name"],
                                print h["threshold-sensor-state"]
                        elif "PSU" in h["sensor-name"]:
                                print h["node-name"],
                                print h["sensor-name"],
                                print h["threshold-sensor-state"]
                        elif "Sysfan1" in h["sensor-name"]:
                                print h["node-name"],
                                print h["sensor-name"],
                                print h["threshold-sensor-state"]
                        elif "SP Status" in h["sensor-name"]:
                                print h["node-name"],
                                print h["sensor-name"],
                                print h["threshold-sensor-state"]
                        else:
                                pass


def failed_disk(s):
        api = NaElement("storage-disk-get-iter")
        api.child_add_string("max-records","1000")

        xi = NaElement("query")
        api.child_add(xi)

        xi.child_add_string("storage-disk-info","<storage-disk-info>")

        xo = s.invoke_elem(api)

        obj = xmltodict.parse(xo.sprintf())
        jd = json.dumps(obj)
        jl = json.loads(jd)

        print "Node             Disk"
        print "====================="
        if xo.results_status() == "failed":
                reason = xo.results_reason()
                print ("Failure: %s" %reason)
        else:
                for h in jl["results"]["attributes-list"]["storage-disk-info"]:
                        if h["disk-ownership-info"]["is-failed"] == "true":
                                print h["disk-ownership-info"]["home-node-name"],
                                print h["disk-name"],
                                print h["disk-ownership-info"]["is-failed"]
                        else:
                                pass



cluster_info(s)
alarm(s)
aggr(s)
vol(s)
sensors(s)
failed_disk(s)
