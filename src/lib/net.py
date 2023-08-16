import urllib.request

class Response:
	def __init__(self, status = None, text = None, headers = None):
		self.status = status or 0
		self.text = text or ""
		self.headers = headers or {}


def fetch(uri, data=None, headers={}):
	request = urllib.request.Request(uri, data, headers)
	page = urllib.request.urlopen(request)
	if page:
		return Response(page.status, page.read(), page.headers)
