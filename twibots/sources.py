"""
	General Sources for the Twibots Platform
	Includes: RssFeed, TwitterSearch, DirectMessageControl
	
	Sources are simple classes, inherited from tb.Sources.
	Every source should have a read() method that yields some result
	or raises a StopIteration exception, since sources are used in
	for loops inside the Twibot objects.
	
	Yielded objects should be constructed using the tb.Writable class.
	Such objects can contain extra data besides the default attributes.
	
	Sources contain so-called actions, which are passed on to channels
	using the writables they produce, for instance, if you'd like the
	TwitterSearch source to retweet the found message and then follow
	it's author, you should assign ['tweet', 'follow'] to the actions
	list, which are appended to every writable it produces.
	
	When the Channels then receive such writables, they know exactly
	what to do with each and every one of them.
"""

import logging
import core as tb
import channels
import extras.feedparser as feedparser
from datetime import datetime
import time

class RssFeed(tb.Source):
	"""
		Uses feedparser.py to parse RSS and Atom feeds. We store a 
		timestamp of the latest feed entry, so that older entries
		are not parsed. This allows us not to repeat ourselves.
	"""
	def __init__(self, feed_url, count=5, actions=['default']):
		"""
			Initializing an RssFeed is easy, simply pass on the
			feed_url and the number of entries you'd like to act upon.
		"""
		self.feed_url = feed_url
		self.count = count
		self.actions = actions
		self.cache = []
	
	def read(self):
		"""
			This method is called by a Twibot. It parses the feed
			entries, converts them into writables and yields the
			results one by one.
		"""

		# Clear cache
		if len(self.cache) > 20:
			self.cache = self.cache[-10:]

		logging.debug("Reading RSS Feed: %s" % self.feed_url)
		feed = feedparser.parse(self.feed_url)
		if not len(feed['entries']):
			logging.error("There's something wrong with the feed: %s" % self.feed_url)
			raise StopIteration

		feed['entries'] = reversed(feed['entries'][:self.count])
		
		for item in feed['entries']:
			
			if item.title in self.cache:
				continue
				
			self.cache.append(item.title)

			tags = []
			try:
				for tag in item.tags:
					tags.append(tag['term'])
			except:
				pass

			writable = tb.Writable(
				title=item.title, 
				permalink=item.link,
				tags=tags
			)
			
			writable.actions = self.actions
			if 'summary' in item: writable.summary=item.summary
			if 'content' in item: writable.content=item.content[0].value
			
			yield writable

class TwitterSearch(tb.Source):
	"""
	
	"""
	def __init__(self, twitter, q, count=10, actions=['default']):
		self.q = q
		self.count = count
		self.api = twitter.api
		self.actions = actions
		self.max_id = 0
	
	def read(self):
		response = self.api.get('search', {'q': self.q, 'rpp': self.count, 'since_id': self.max_id})
		self.max_id= response['max_id']
		results = response['results']
		
		for tweet in results:
			writable = tb.Writable(title=tweet['text'], author=tweet['from_user'])
			writable.tweet_id = tweet['id']
			writable.actions = self.actions
			yield writable

if __name__ == '__main__':
	feed = RssFeed(feed_url='http://www.google.com/reader/public/atom/user/08886841141873836783/state/com.google/broadcast')
	while(True):
		for entry in feed.read():
			print entry.title
			
		time.sleep(1)
		
	exit()
	
	# Please don't abuse these
	CONSUMER_KEY = 'Ai5tJWvg0UEnPNzOoDrP8A'
	CONSUMER_SECRET = 'LAWbNw7ovHBHES6ymBLCWjx28oZT3wLRRB8PBV7sk'
	twitter = channels.Twitter(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
	search = TwitterSearch(twitter, q='#wordpress', count=5)
	for writable in search.read():
		print writable
