class CheatSheet():
	"""CheatSheet represents each individual cheatsheet"""
	def __init__(self, name, filename, description, platform):
		self.name = name
		self.filename = filename
		self.description = description
		self.platform = platform

	def __str__(self):
		return self.name
	def __cmp__(self, other):
		return cmp(self.name, other.name)