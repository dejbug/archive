import re, urllib.parse

import lib.abs

@lib.abs.stringify
@lib.abs.dumpify
class Uri:

	def init(self, text):
		self.text = text
		x = urllib.parse.urlparse(text)
		# self.x = x
		self.ok = False
		self.scheme = x.scheme
		self.host = x.netloc
		self.path = x.path
		self.params = x.params
		self.query = urllib.parse.parse_qsl(x.query) if x.query else None
		self.fragment = x.fragment

		self.type = None
		self.root = None
		self.user = None
		self.file = None

	def __bool__(self):
		return self.ok

	@property
	def ext(self):
		if self.file:
			return os.path.splitext(self.file)

	@property
	def index(self):
		if self.root:
			return self.parse(f'{self.scheme}://{self.host}/download/{self.root}/{self.root}_files.xml')
		return self.parse('')

	@property
	def listing(self):
		if self.root:
			return self.parse(f'{self.scheme}://{self.host}/download/{self.root}')
		return self.parse('')

	@property
	def details(self):
		if self.root:
			return self.parse(f'{self.scheme}://{self.host}/details/{self.root}')
		return self.parse('')

	@classmethod
	def parse(cls, text):
		uri = cls()
		uri.init(text)

		m = re.match(r'/(download|details|search)(/.+)?', uri.path)
		if not m:
			uri.ok = False
			return uri

		uri.ok = True
		uri.type = m.group(1)

		pp = uri.path.strip('/').split('/')

		if uri.type == 'download':
			if len(pp) == 2:
				uri.type = 'listing'
				uri.root = pp[1]
			elif len(pp) == 3:
				uri.type = 'file'
				uri.root = pp[1]
				uri.file = pp[2]
				print(uri.file)
				if uri.file.endswith(f'{uri.root}/_files.xml'):
					uri.type = 'index'
				pass
		elif uri.type == 'details':
			assert len(pp) >= 2
			if pp[1].startswith('@'):
				uri.type = 'user'
				uri.user = pp[1].strip('@')
			else:
				uri.root = pp[1]

		return uri


parse = Uri.parse


def text(uri):
	return uri.text if isinstance(uri, Uri) else str(uri)
