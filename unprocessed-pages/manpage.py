class ManPage():
	"""ManPage represents each individual man page"""
	def __init__(self, name, folder, section, filename, description):
		self.name = name
		self.folder = folder
		self.section = section
		self.filename = filename
		self.description = description

	def __str__(self):
		return self.name
	def __cmp__(self, other):
		return cmp(self.name, other.name)