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

class TagsToHashtags(tb.Filter):
	"""
		Scans through the tags argument of a Writable object and appends
		the hash symbol # to every one of them. Please use this filter after
		inline hashtags.
	"""
	
	def filter(self, writable):
		tags = []
		for tag in writable.tags:
			tags.append('#%s' % tag)
			
		writable.tags = tags
		return writable

		
class InlineHashtags(tb.Filter):
	"""
		Inline hashtags filter, mainly for the Twitter channel, can search for
		and replace tags with hashtags, assuming they're listed in the tags
		attribute of the Writable object. The returned writable object's tags
		attribute is left with tags that were not replaced inline (remaining).
	"""
	
	def filter(self, writable):
		original = writable.title
		letters = list(original)
		remaining = []
		for tag in writable.tags:
			pos = original.lower().find(tag)
			if pos > -1:
				letters.insert(pos, '#')
				original = ''.join(letters)
			else:
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
	bitly = Bitly(username='kovshenin', api_key='R_9f3bde0c5e2d36a3e747490bb37a6d5d')
	writable = tb.Writable(permalink='http://kovshenin.com')
	print bitly.filter(writable)

	trim = Trim140(max_length=120)
	t2h = TagsToHashtags()
	inline = InlineHashtags()
	
	writable = tb.Writable(title="Lorem Ipsum Dolor Sit Amet, Bleh Beh Meh Dududeh Lorem Ipsum Dolor sit Amet Good Bad TechCrunch Mashable", excerpt="Excerpt", content="Content", tags=['lorem', 'dolor', 'google', 'boogle', 'nice', 'tech'], permalink='http://kovshenin.com')
	writable = inline.filter(writable)
	writable = t2h.filter(writable)
	writable = trim.filter(writable)
	
	print len(writable.output), writable.output
