import urllib2
import sys
import xml.etree.ElementTree as ET
APIKEY = 'AnWEcUQfXEU--HBIE1-9O3mef3vzrjbdyK0J7vjFc6lfqXCa8BoqHgcHbMSpTDkf'

#get routes
url = 'http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0='
origin = sys.argv[1] + "," + sys.argv[2]
dest = sys.argv[3]
request = url + origin + '&wp.1=' + dest + '&maxSolns=3&key=' + APIKEY
#origin = sys.argv[1] + "," + sys.argv[2]
#dest = sys.argv[3]
#request = url + origin + '&destination=' + dest + '&alternatives=true&key=' + APIKEY

#request = 'http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0=wroclaw&wp.1=paris&maxSolns=3&key='+APIKEY
response = urllib2.urlopen(request)
html = response.read()


routes = []
durations = []
distances = []
traffic = []
root = ET.fromstring(html)
ResourceSets = root.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}ResourceSets')
ResourceSet = ResourceSets.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}ResourceSet')
Resources = ResourceSet.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}Resources')
for route in Resources.findall('{http://schemas.microsoft.com/search/local/ws/rest/v1}Route'):
    routes.append(route)
    durations.append(route.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}TravelDuration'))
    distances.append(route.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}TravelDistance'))
    traffic.append(route.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}TrafficCongestion'))

for i in range(len(routes)):
    print str(i) + ';' + str(float(durations[i].text) /3600) + ';' +str(float(distances[i].text) / 1000) + ';' + traffic[i].text + "\n"



