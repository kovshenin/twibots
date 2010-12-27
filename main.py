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
	
class Source():
	"""
		Sources can be anything, from RSS/Atom feeds to Twitter Searches,
		Google News, etc. Make sure that Sources yield results when reading.
	"""
	def read(self):
		raise NotImplementedError
		
class RssFeed(Source):
	def __init__(self, feeds=[]):
		self.feeds = feeds
	
	def read(self):
		for feed in self.feeds:
			writable = Writable(title='Some title goes here', permalink=feed, tags=['title', 'here'])
			yield writable
			
class Filter():
	def filter(self):
		raise NotImplementedError

class Bitly(Filter):
	def filter(self, writable):
		writable.permalink = 'http://bit.ly/short'
		return writable
		
class InlineHashtags(Filter):
	"""
		Inline hashtags filter, mainly for the Twitter channel, can search for
		and replace tags with hashtags, assuming they're listed in the tags
		attribute of the Writable object.
	"""
	def filter(self, writable):
		for tag in writable.tags:
			writable.title = writable.title.replace(tag, '#%s' % tag)
			
		return writable

class Channel():
	filters = []
	
	def write(self):
		raise NotImplementedError
		
	def read(self):
		raise NotImplementedError

class Twitter(Channel):
	def write(self, writable):
		writable = self.filter(writable)
		print "Tweeting: %s %s" % (writable.title, writable.permalink)

	# Run the associated filters (note: can be inherited)
	def filter(self, writable):
		for filter in self.filters:
			writable = filter.filter(writable)
			
		return writable

# Self-test code
if __name__ == '__main__':
	twibot = Twibot()
	
	twitter = Twitter()
	twitter.filters.append(Bitly())
	twitter.filters.append(InlineHashtags())
	
	rss = RssFeed(feeds=['http://kovshenin.com/feed', 'http://mashable.com/feed'])
	
	twibot.sources.append(rss)
	twibot.channels.append(twitter)

	twibot.live()
