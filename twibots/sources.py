import core as tb
import channels
import extras.feedparser as feedparser

class RssFeed(tb.Source):
	def __init__(self, feed_url, count=5, actions=['default']):
		self.feed_url = feed_url
		self.count = count
		self.actions = actions
	
	def read(self):
		feed = feedparser.parse(self.feed_url)
		i = 0
		for item in feed['entries']:
			
			# Let's see if we got more than self.count allowed.
			i += 1
			if i > self.count:
				raise StopIteration
			
			tags = []
			for tag in item.tags:
				tags.append(tag['term'])

			writable = tb.Writable(
				title=item.title, 
				permalink=item.link,
				tags=tags
			)
			
			writable.actions = self.actions
			
			yield writable

class TwitterSearch(tb.Source):
	def __init__(self, twitter, q, count=10, actions=['default']):
		self.q = q
		self.count = count
		self.api = twitter.api
		self.actions = actions
		#super(TwitterSearch, self).__init__(*args, **kwargs)
	
	def write(self):
		raise NotImplementedError
		
	def read(self):
		response = self.api.get('search', {'q': self.q, 'rpp': self.count})
		results = response['results']
		
		for tweet in results:
			writable = tb.Writable(title=tweet['text'], author=tweet['from_user'])
			writable.tweet_id = tweet['id']
			writable.actions = self.actions
			yield writable

if __name__ == '__main__':
	"""
	feed = RssFeed(feed_url='http://techcrunch.com/feed')
	for entry in feed.read():
		print entry.title
	"""
	# Please don't abuse these
	CONSUMER_KEY = 'cKlpH5jndEfrnhBQrrp8w'
	CONSUMER_SECRET = 'reeYtKhTY7LRTwzXE5tmFrxwkD4lLVY9FgxrY5KFsE'

	search = TwitterSearch(q='wordpress', count=5, consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
	for writable in search.read():
		print writable
