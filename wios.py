__author__ = 'Michal Kosinski'

import requests
import json

req_url = 'http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/pobierz'
req_headers = {
    'Accept'           : 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding'  : 'gzip, deflate',
    'Accept-Language'  : 'pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4',
    'Connection'       : 'keep-alive',
    'Content-Type'     : 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host'             : 'monitoring.krakow.pios.gov.pl',
    'Origin'           : 'http://monitoring.krakow.pios.gov.pl',
    'Referer'          : 'http://monitoring.krakow.pios.gov.pl/dane-pomiarowe/automatyczne/stacja/5/parametry/31-36-34-30-32/dzienny/16.05.2015',
    'User-Agent'       : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'X-Requested-With' : 'XMLHttpRequest'
#    ,'Cookie'           : 'start_selector_nth=0; start_selector_hide=yes'
}

query = {
    "measType"         : "Auto",
    "viewType"         : "Station",
    "dateRange"        : "Day",
    "date"             : "17.05.2015",
    "viewTypeEntityId" : "5",
    "channels"         : [31,36,34,30,32]
}

# r = requests.post(url, data=json.dumps(payload), headers=headers)
#print json.dumps(query)
xx = "query=%7B%22measType%22%3A%22Auto%22%2C%22viewType%22%3A%22Station%22%2C%22dateRange%22%3A%22Day%22%2C%22date%22%3A%2217.05.2015%22%2C%22viewTypeEntityId%22%3A%225%22%2C%22channels%22%3A%5B31%2C36%2C34%2C30%2C32%5D%7D"
#r = requests.post(req_url, headers = req_headers, data = "query=%7B%22measType%22%3A%22Auto%22%2C%22viewType%22%3A%22Station%22%2C%22dateRange%22%3A%22Day%22%2C%22date%22%3A%2230.05.2015%22%2C%22viewTypeEntityId%22%3A7%2C%22channels%22%3A%5B49%2C54%2C61%2C57%2C211%2C53%2C50%2C55%5D%7D")
#r = requests.post(req_url, headers = req_headers, json=query)
#print r.headers
#print r.content
#print "headers: {}\nstatus: {}\n{}".format(r.headers, r.status_code, r.text)

#from urllib import urlopen
import urllib, pprint
#print urllib.unquote(xx).split("=")[1]
zz = json.loads(urllib.unquote(xx).split("=")[1])
#pprint.pprint(zz)
yy = "query=" + urllib.quote(json.dumps(zz,separators=(",",":")))
yyyy = json.loads(urllib.unquote(yy).split("=")[1])
pprint.pprint(yyyy)
print xx + "\n" + yy
#x = urlopen(req_url, data = json.dumps(query))
#print x.readlines()
r = requests.post(req_url, headers = req_headers, data = yy)
print r.content

"query=%7B%22measType%22%3A%22Auto%22%2C%22viewType%22%3A%22Station%22%2C%22dateRange%22%3A%22Day%22%2C%22date%22%3A%2217.05.2015%22%2C%22viewTypeEntityId%22%3A%225%22%2C%22channels%22%3A%5B31%2C36%2C34%2C30%2C32%5D%7D"
"query=%7B%22viewTypeEntityId%22%2C%225%22%3A%22dateRange%22%2C%22Day%22%3A%22channels%22%2C%5B31%3A36%3A34%3A30%3A32%5D%3A%22date%22%2C%2217.05.2015%22%3A%22viewType%22%2C%22Station%22%3A%22measType%22%2C%22Auto%22%7D"