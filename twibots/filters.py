import core as tb
import urllib, urllib2
import simplejson

class Bitly(tb.Filter):
	def __init__(self, username, api_key):
		self.username = username
		self.api_key = api_key
		
	def filter(self, writable):
		data = urllib.urlencode({'login': self.username, 'apiKey': self.api_key, 'format': 'json', 'longUrl': writable.permalink})
		response = urllib2.urlopen('http://api.bit.ly/v3/shorten', data)
		response = simplejson.loads(response.read())
		if response['status_code'] == 200:
			writable.permalink = response['data']['url']

		return writable
		
class NoRetweets(tb.Filter):
	def filter(self, writable):
		if 'rt' in writable.title.lower().split():
			return tb.Writable()
		else:
			return writable
			
class NoDuplicates(tb.Filter):
	"""
		Requires the Levenshtein module.
	"""
	def __init__(self, threshold=0.60, cache_size=200):
		self.threshold = threshold
		self.cache = []
		self.cache_size = cache_size

	def filter(self, writable):
		import Levenshtein
		
		if len(self.cache) > self.cache_size:
			self.cache = self.cache[-self.cache_size:]
		
		for item in self.cache:
			if Levenshtein.ratio(str(item), str(writable.title)) > self.threshold:
				print "Duplicate detected: \"%s\" matched \"s%s\" with a score of %s" % (writable.title, item, Levenshtein.ratio(str(item), str(writable.title)))
				return tb.Writable()
				
		self.cache.append(writable.title)
		return writable
		
class NoLinks(tb.Filter):
	def filter(self, writable):
		if 'http://' in writable.title.lower():
			return tb.Writable()
		else:
			return writable
			
class NoMentioins(tb.Filter):
	def filter(self, writable):
		if '@' in writable.title:
			return tb.Writable()
		else:
			return writable
			
class NoHashtags(tb.Filter):
	def filter(self, writable):
		if '#' in writable.title:
			return tb.Writable()
		else:
			return writable

class TagsToHashtags(tb.Filter):
	"""
		Scans through the tags argument of a Writable object and appends
		the hash symbol # to every one of them. Please use this filter after
		inline hashtags.
	"""
	
	def filter(self, writable):
		tags = []
		for tag in writable.tags:
			if ' ' not in tag and '-' not in tag:
				tags.append('#%s' % tag.lower())
			
		writable.tags = tags
		return writable

		
class InlineHashtags(tb.Filter):
	"""
		Inline hashtags filter, mainly for the Twitter channel, can search for
		and replace tags with hashtags, assuming they're listed in the tags
		attribute of the Writable object. The returned writable object's tags
		attribute is left with tags that were not replaced inline (remaining).
		
		Additional tags could be passed to the filter duruing __init__, these
		will not be appended to the final writable.tags list (remaining) but
		will be inlined.
	"""
	def __init__(self, additional_tags=[]):
		self.additional_tags = additional_tags
	
	def filter(self, writable):
		original = writable.title
		letters = list(original)
		remaining = []
		for tag in writable.tags + self.additional_tags:
			
			# Let's see if there's already such a hashtag in the title
			if '#%s' % tag in original.lower():
				continue
			
			pos = original.lower().find(tag)
			if pos > -1:
				letters.insert(pos, '#')
				original = ''.join(letters)
			else:
				if tag in writable.tags:
					remaining.append(tag)
				
		writable.title = ''.join(letters)
		writable.tags = remaining

		return writable

class Trim140PermalinkTooLong(): pass
class Trim140(tb.Filter):
	"""
		Use this filter to produce tweets. It scans a Writable object and returns
		it with an extra attribute "output" which contains the text trimmed down
		to 140 (or other via options) characters based on a specific pattern
	"""
	
	def __init__(self, max_length=140):
		self.max_length = max_length
	
	def filter(self, writable):
		# This won't loop forever
		while True:
			# Loop while our length is not less or equal to max length
			if len(self.construct(writable.title, writable.permalink, writable.tags)) <= self.max_length:
				break
			
			# Do we have any hashtags left?
			if len(writable.tags):
				writable.tags = writable.tags[:-1]#.remove(len(writable.tags))
				continue
				
			# Start shoreting the title (by removing single words)
			if len(writable.title):
				writable.title = ' '.join(writable.title.split()[:-1])
				continue
				
			# If the statements above have failed to "continue", then the tweet
			# cannot be reduced anymore, thus we state that the permalink is too long.
			raise Trim140PermalinkTooLong

		# Format the final string, attach to the Writable and return
		writable.output = self.construct(writable.title, writable.permalink, writable.tags)
		return writable
		
	def construct(self, title, permalink, tags=[]):
		"""
			Construct the final string using the specified format.
		"""
		s = "%s %s %s" % (title, permalink, ' '.join(tags))
		return s.strip()

# Self-test code.
if __name__ == '__main__':
	# Bitly
	print "Bitly()"
	bitly = Bitly(username='kovshenin', api_key='R_9f3bde0c5e2d36a3e747490bb37a6d5d')
	writable = tb.Writable(permalink='http://kovshenin.com')
	print "Long link: http://kovshenin.com"
	print "Shortened: %s" % bitly.filter(writable).permalink
	print
	
	# NoRetweets
	print "NoRetweets()"
	writables = [tb.Writable(title="Text"), tb.Writable(title="RT Text"), tb.Writable(title="rt text"), tb.Writable(title="rting text")]
	nort = NoRetweets()
	print "Input:"
	for writable in writables:
		print "\t%s" % writable.title
		
	print "Output:"
	for writable in writables:
		writable = nort.filter(writable)
		if writable.title:
			print "\t%s" %  writable.title
			
	print
	
	# NoDuplicates
	print "NoDuplicates()"
	writables = [
		tb.Writable(title="8 Gadgets to Watch in 2011 - http://on.mash.to/giO5HX"),
		tb.Writable(title="Creating a safer email environment http://bit.ly/fk34LG #admin"),
		tb.Writable(title="LivingSocial: #Groupon's Not The Only Company That Can Hire A CFO http://tcrn.ch/fc1xne #tc"),
		tb.Writable(title="#Android App Development - Using Android resources part 1: String Resources http://bit.ly/gRKe52"),
		tb.Writable(title="RT @mashable: 8 #Gadgets to Watch in 2011 - http://bit.ly/123456"),
		tb.Writable(title="LivingSocial: Groupon Can Hire a Company CFO: http://bit.ly/99921"),
	]
	nodups = NoDuplicates()
	print "Input:"
	for writable in writables:
		print "\t%s" % writable.title
		
	print "Output:"
	for writable in writables:
		writable = nodups.filter(writable)
		if writable.title:
			print "\t%s" %  writable.title
			
	print
	
	exit()
	
	trim = Trim140(max_length=120)
	t2h = TagsToHashtags()
	inline = InlineHashtags()
	
	writable = tb.Writable(title="#Mashable", excerpt="Excerpt", content="Content", tags=['mashable awards', 'lorem', 'dolor', 'Google', 'boogle', 'nice', 'tech'], permalink='http://kovshenin.com')
	writable = inline.filter(writable)
	writable = t2h.filter(writable)
	writable = trim.filter(writable)
	
	print len(writable.output), writable.output
