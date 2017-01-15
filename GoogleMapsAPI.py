#import urllib2
#import json
#import pprint
APIKEY = 'AIzaSyCyAIzXNWswpGkm6fATebPuzTBjfAJivWo'

import urllib2
import xml.etree.ElementTree as ET
import sys

#get routes
url = 'https://maps.googleapis.com/maps/api/directions/xml?origin='
origin = sys.argv[1] + "," + sys.argv[2]
dest = sys.argv[3]
request = url + origin + '&destination=' + dest + '&alternatives=true&key=' + APIKEY


response = urllib2.urlopen(request)
html = response.read()


root = ET.fromstring(html)
routes = []
durations = []
distances = []
for route in root.findall('./route'):
    routes.append(route)
    durations.append(route.find('leg/duration/value'))
    distances.append(route.find('leg/distance/value'))

for i in range(len(routes)):
    print str(i) + ';' + str(float(durations[i].text) /3600) + ';' +str(float(distances[i].text) / 1000) + "\n"








