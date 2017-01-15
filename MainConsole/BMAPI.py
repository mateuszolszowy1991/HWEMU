import urllib2
import sys, os
import xml.etree.ElementTree as ET


class BMAPI:

	APIKEY='AnWEcUQfXEU--HBIE1-9O3mef3vzrjbdyK0J7vjFc6lfqXCa8BoqHgcHbMSpTDkf'

	def __init__(self):
		self.url='http://dev.virtualearth.net/REST/V1/Routes/Driving?o=xml&wp.0='

	def setData(self,src,dest):
		self.origin=src
		self.dest=dest
		self.request=self.url+self.origin+'&wp.1='+self.dest+'&key='+self.APIKEY

	def sendRequest(self):
		self.response=urllib2.urlopen(self.request)
		self.html=self.response.read()

	def prepareResult(self):
		self.root = ET.fromstring(self.html)
		self.ResourceSets = self.root.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}ResourceSets')
		self.ResourceSet = self.ResourceSets.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}ResourceSet')
		self.Resources = self.ResourceSet.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}Resources')
		self.getRouteInformation()

	def getRouteInformation(self):
		self.route = self.Resources.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}Route')
		self.RouteLeg = self.route.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}RouteLeg')
		self.startLocation = self.RouteLeg.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}StartLocation').find('{http://schemas.microsoft.com/search/local/ws/rest/v1}Name')
		self.endLocation = self.RouteLeg.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}EndLocation').find('{http://schemas.microsoft.com/search/local/ws/rest/v1}Name')
		self.durations = self.route.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}TravelDuration')
		self.distances = self.route.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}TravelDistance')
		self.traffic = self.route.find('{http://schemas.microsoft.com/search/local/ws/rest/v1}TrafficCongestion')

	def printResults(self):
		self.saveResultToFile("Target\n")
		self.saveResultToFile(self.startLocation.text.encode('utf-8') + ';' + self.endLocation.text.encode('utf-8') + ';' + str(float(self.durations.text) /3600.0).encode('utf-8') + ';' +str(float(self.distances.text)).encode('utf-8') + ';' + self.traffic.text.encode('utf-8') + "\n")

	def ifFileExistRemoveIt(self):
		if(os.path.isfile("/home/mato3/OSCAR/SYS/TEMP/routes.txt")):
			os.unlink("/home/mato3/OSCAR/SYS/TEMP/routes.txt")

	def saveResultToFile(self, result):
		f = open("/home/mato3/OSCAR/SYS/TEMP/routes.txt", "a")
		f.write(result)
		f.close()

	def translate(self, sign):
		if sign == "ABCDE":
			return [1, 5, 8, 10]
		elif sign == "ACBDE":
			return [2, 5, 6, 10]
		elif sign == "ACDBE":
			return [2, 8, 6, 7]
		elif sign == "ABDCE":
			return [1, 6, 8, 9]
		elif sign == "ADBCE":
			return [3, 6, 5, 9]
		elif sign == "ABECD":
			return [1, 7, 9, 8]
		elif sign == "AEBCD":
			return [4, 9, 5, 8]
		else:
			print "BMAPI: Translate: err"
			return []
            
