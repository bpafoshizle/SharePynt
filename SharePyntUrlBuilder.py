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
		return url
		
	def buildUploadFileUrl(self, library, file):
		url = self.SiteUrl + "/_api/Web/GetFileByServerRelativeUrl('/" + self.Site + "/" + library + "/" + file + "')/$value"		
		return url		
		
	def buildCheckOutFileUrl(self, library, file):
		url = self.SiteUrl + "/_api/Web/GetFileByServerRelativeUrl('/" + self.Site + "/" + library + "/" + file + "')/checkout()"
		return url

	def buildCheckInFileUrl(self, library, file, comment):
		url = self.SiteUrl + "/_api/Web/GetFileByServerRelativeUrl('/" + self.Site + "/" + library + "/" + file + "')/checkin(comment='" + comment + "',checkintype=0)"	
		return url
			
	def buildContextInfoUrl(self):
		url = self.SiteUrl + "/_api/contextinfo"
		return url
		