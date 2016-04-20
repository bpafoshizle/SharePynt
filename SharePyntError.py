class CheckoutError(Exception):
	def __init__(self, value):
	 self.value = value
	def __str__(self):
	 return repr(self.value)
	 
class CheckinError(Exception):
	def __init__(self, value):
	 self.value = value
	def __str__(self):
	 return repr(self.value)
	 
class UploadError(Exception):
	def __init__(self, value):
	 self.value = value
	def __str__(self):
	 return repr(self.value)
	 
class DownloadError(Exception):
	def __init__(self, value):
	 self.value = value
	def __str__(self):
	 return repr(self.value)
	 
class DigestAquisitionError(Exception):
	def __init__(self, value):
	 self.value = value
	def __str__(self):
	 return repr(self.value)	 