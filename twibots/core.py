class Twibot():
	sources = []
	filters = []
	channels = []
	
	def __init__(self, name=None):
		self.name = None
		pass
		
	def live(self):
		for source in self.sources:
			for writable in source.read(): #has to yield
				for channel in self.channels:
					channel.write(writable)
		
	def rest(self):
		pass

class Readable():
	pass

class Writable():
	def __init__(self, title='', excerpt='', content='', permalink='', author='', tags=[]):
		self.title = title
		self.excerpt = excerpt
		self.content = content
		self.permalink = permalink
		self.author = author
		self.tags = tags
		
	def __str__(self):
		return "Writable: %s" % ''.join(['\n\t%s=%s' % (k,repr(v)) for k,v in self.__dict__.iteritems()])
	
class Source():
	"""
		Sources can be anything, from RSS/Atom feeds to Twitter Searches,
		Google News, etc. Make sure that Sources yield results when reading.
	"""
	def read(self):
		raise NotImplementedError
		
class Filter():
	def filter(self):
		raise NotImplementedError

class Channel():
	filters = []
	
	def write(self):
		raise NotImplementedError
		
	def read(self):
		raise NotImplementedError

	# Run the associated filters (note: can be inherited)
	def filter(self, writable):
		for filter in self.filters:
			writable = filter.filter(writable)
			
		return writable

# Self-test code
if __name__ == '__main__':
	twibot = Twibot()
	
	twibot.filters.append(Filter())
	twibot.sources.append(Source())
	twibot.channels.append(Channel())

	twibot.live()
