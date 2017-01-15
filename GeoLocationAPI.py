import urllib2
import xml.etree.ElementTree as ET

request = 'http://ip-api.com/xml'
response = urllib2.urlopen(request)
html = response.read()
root = ET.fromstring(html)
latitude = root.findall('./lat')
longitude = root.findall('./lon')

print latitude[0].text
print longitude[0].text