class SharePyntUrlBuilder:
	""" Helper class for building URLs """
	def __init__(self, server, site):
		self.Server = server.strip("/")
		self.Site = site.strip("/")
		self.SiteUrl = self.buildSiteUrl()
	
	def buildSiteUrl(self):
		return "http://" + self.Server + "/" + self.Site
		
	def buildDownloadFileUrl(self, library, file):
		url = self.SiteUrl + "/_api/Web/GetFileByServerRelativeUrl('/" + self.Site + "/" + library + "/" + file + "')/$value"
		print("Download URL: %s" % (url))
		return url
		
	def buildUploadFileUrl(self, library, file):
		url = self.SiteUrl + "/_api/Web/GetFileByServerRelativeUrl('/" + self.Site + "/" + library + "/" + file + "')/$value"		
		print("Upload URL: %s" % (url))
		return url		
		
	def buildCheckOutFileUrl(self, library, file):
		url = self.SiteUrl + "/_api/Web/GetFileByServerRelativeUrl('/" + self.Site + "/" + library + "/" + file + "')/checkout()"
					
		print("Checkout URL: %s" % (url))
		return url

	def buildCheckInFileUrl(self, library, file, comment):
		url = self.SiteUrl + "/_api/Web/GetFileByServerRelativeUrl('/" + self.Site + "/" + library + "/" + file + "')/checkin(comment='" + comment + "',checkintype=0)"	
		print("Checkin URL: %s" % (url))
		return url
			
	def buildContextInfoUrl(self):
		url = self.SiteUrl + "/_api/contextinfo"
		print("Context URL: %s" % (url))
		return url
		