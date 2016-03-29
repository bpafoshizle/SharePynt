class SharePynt:
	""" A class to make working with Microsoft SharePoint from Python Easier """
	
	def __init__(self, server, site, authType):
		import requests
		self.Server = server.strip("/")
		self.authType = authType
		self.Site = site.strip("/")
		self.SiteUrl = self.buildSiteUrl()
		self.session = requests.Session()
		self.session.auth = self.getAuth()
				
	def UploadFile(self, library, file):
		return None
		# implement
	
	def DownloadFile(self, library, file, localFileName):
		url = self.buildDownloadFileUrl(library, file)
		print("Downloading %s" % url)
		r = self.session.get(url,stream=True)
		with open(localFileName, 'wb+') as f:
			for chunk in r.iter_content(chunk_size=1024): 
				if chunk:
					f.write(chunk)
					f.flush()
		return None
		# implement
		
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
					
	def buildSiteUrl(self):
		return "http://" + self.Server + "/" + self.Site
		
	def buildDownloadFileUrl(self, library, file):
		return self.SiteUrl + "/_api/Web/GetFileByServerRelativeUrl('/" + self.Site + "/" + library + "/" + file + "')/$value"
		
	
		
		

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('server')
	parser.add_argument('site')
	parser.add_argument('authType')
	args = parser.parse_args()
	
	sp = SharePynt(args.server,args.site,args.authType)
	print("User: %s, Pass: %s" % (sp.credDict["u"], sp.credDict["p"]))
	print("Site URL: %s" % (sp.SiteUrl))
	sp.DownloadFile("Supply Chain Order Tracking", "CORE - SC - STO.xlsx", "CORE - SC - STO.xlsx")
	