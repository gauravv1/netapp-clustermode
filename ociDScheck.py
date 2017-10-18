import requests
import requests.packages.urllib3
import sys
from datetime import timedelta, datetime
from asn1crypto.core import Null
from formatter import NullWriter

requests.packages.urllib3.disable_warnings()

dc = sys.argv[1]

def retrive_storage(name,dc):
    ''' this is function to check if data source is failed and what was last acquition time'''
    r = requests.get('https://onaro-'+ str(dc) + '/rest/v1/admin/datasources', auth=('gauravv@cisco.com','*********'),verify=False)
    s = requests.get('https://onaro-'+ str(dc) + '/rest/v1/login',auth=('guest','guest'),verify=False)
    for storage in r.json():
        if storage['status'] == 'FAILED':
                print storage['name'],
                print storage['status'],
                print storage['statusText'],

                date = storage['lastSuccessfullyAcquired'].split("T")[0]
                time = storage['lastSuccessfullyAcquired'].split("T")[1].split("-")[0]
                last_acq = storage['lastSuccessfullyAcquired'].split("T")[0] + " %s" %storage['lastSuccessfullyAcquired'].split("T")[1].split("-")[0]
                today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                FMT = '%Y-%m-%d %H:%M:%S'
                tdelta = datetime.strptime(today, FMT) - datetime.strptime(last_acq, FMT)
                print tdelta

retrive_storage('ss',dc)
