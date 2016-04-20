class SharePynt:
	""" A class to make working with Microsoft SharePoint from Python Easier """
	
	def __init__(self, server, site, authType, logLevel=0):
		import requests
		import logging
		from SharePyntUrlBuilder import SharePyntUrlBuilder
		self.urlBuilder = SharePyntUrlBuilder(server, site)
		self.authType = authType
		self.session = requests.Session()
		self.session.auth = self.getAuth()
		
		# Logging
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logLevel)
		fh = logging.FileHandler('Log/debug.log')
		fh.setLevel(logging.DEBUG)
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)
		self.logger.addHandler(fh)
		self.logger.addHandler(ch)
				
	def UploadFile(self, library, file, localFileName):
		import sys
		
		# Set up context 
		self.getContext()
		headers = {"X-RequestDigest":self.formDigestValue}
			
		#Checkout
		self.CheckOutFile(library, file, self.ctxResponse)
			
		# Upload
		url = self.urlBuilder.buildUploadFileUrl(library, file)
		with open(localFileName, 'rb') as f:
			r = self.session.put(url, data = f, headers=headers)
			# Make sure upload is successful
			if r.status_code != 204:
				from SharePyntError import UploadError
				raise UploadError("Upload unsuccessful with return code %s" % (r.status_code))
		
		self.logger.debug("Uploaded. Status code %s.", r.status_code)
			#fileData = f.read()
		#self.logger.debug("Read %d bytes of file %s", sys.getsizeof(fileData), localFileName)
		
		
		
		#Checkin
		self.CheckInFile(library, file, self.ctxResponse)
		
		return None

	def CheckOutFile(self, library, file, context=None):
		if(context == None):#TODO: Also check for expiration
			self.getContext()
					
		# Check out
		headers = {"X-RequestDigest":self.formDigestValue}	
		url = self.urlBuilder.buildCheckOutFileUrl(library, file)
		r = self.session.post(url, headers=headers)
					
		# Make sure checkout is successful
		if r.status_code != 200:
			from SharePyntError import CheckoutError
			raise CheckoutError("Checkout unsuccessful with return code %s" % (r.status_code))
		self.logger.debug("Checked out. Status code %s", r.status_code)
		

	def CheckInFile(self, library, file, context=None):
		if(context == None):#TODO: Also check for expiration
			self.getContext()
		
		# Check In
		headers = {"X-RequestDigest":self.formDigestValue}
		url = self.urlBuilder.buildCheckInFileUrl(library, file, comment="Checked in from SharePynt Python Library.")
		r = self.session.post(url, headers=headers)
		
		# Make sure checkin is successful
		if r.status_code != 200:
			from SharePyntError import CheckinError
			raise CheckinError("Checkin unsuccessful with return code %s" % (r.status_code))
		self.logger.debug("Checked in. Status code %s", r.status_code)
	
	def DownloadFile(self, library, file, localFileName):
		url = self.urlBuilder.buildDownloadFileUrl(library, file)
		self.logger.debug("Downloading %s" , url)
		r = self.session.get(url,stream=True)
		with open(localFileName, 'wb+') as f:
			for chunk in r.iter_content(chunk_size=1024): 
				if chunk:
					f.write(chunk)
					f.flush()
		return None
		
	def GetUrlXml(self, serverUrl):
		return None
		# implement
		
	def readCredentials(self, credFilePath):
		""" Expects username with domain on first line, password on second line """
		self.credDict = {}
		with open(credFilePath, "r") as f:
			self.credDict["u"] = f.readline().strip()
			self.credDict["p"] = f.readline().strip()
		
		return self.credDict
		
	def getAuth(self):
		if self.authType == "basic":
			self.readCredentials("Sensitive/basicCreds.txt")
			from requests.auth import HTTPBasicAuth
			return HTTPBasicAuth(self.credDict["u"], self.credDict["p"])
		elif self.authType == "ntlm":
			self.readCredentials("Sensitive/domainCreds.txt")
			from requests_ntlm import HttpNtlmAuth
			return HttpNtlmAuth(self.credDict["u"], self.credDict["p"])
			
	def getContext(self):
		url = self.urlBuilder.buildContextInfoUrl()
		self.ctxResponse = self.session.post(url)
		from bs4 import BeautifulSoup
		doc = BeautifulSoup(self.ctxResponse.text)
		
		if doc.find("d:formdigestvalue") == None:
			from SharePyntError import DigestAquisitionError
			raise DigestAquisitionError("Unable to obtain form digest information.")
		else:
			self.formDigestValue = doc.find("d:formdigestvalue").string
			
		self.logger.debug("Digest aquired: %s", self.formDigestValue)
		
		

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('server')
	parser.add_argument('site')
	parser.add_argument('authType')
	args = parser.parse_args()
	
	sp = SharePynt(args.server,args.site,args.authType,10)
	#sp.DownloadFile("Supply Chain Order Tracking", "CORE - SC - STO.xlsx", "CORE - SC - STO.xlsx")
	sp.UploadFile("Supply Chain Order Tracking", "CORE - SC - STO.xlsx", "C:\\Users\\Millerbarr\\Documents\\SAP\\HANA SAP to SIM Compare\\Daily Reports\\AutoRefresh\\Reports\\CORE - SC - STO.xlsx")
	