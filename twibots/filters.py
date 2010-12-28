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
		
class InlineHashtags(tb.Filter):
	"""
		Inline hashtags filter, mainly for the Twitter channel, can search for
		and replace tags with hashtags, assuming they're listed in the tags
		attribute of the Writable object.
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

# Self-test code.
if __name__ == '__main__':
	bitly = Bitly(username='kovshenin', api_key='R_9f3bde0c5e2d36a3e747490bb37a6d5d')
	writable = tb.Writable(permalink='http://kovshenin.com')
	print bitly.filter(writable)
