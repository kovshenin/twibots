import core as tb
import extras.feedparser as feedparser

class RssFeed(tb.Source):
	def __init__(self, feed_url, count=5):
		self.feed_url = feed_url
		self.count = count
	
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
			yield writable

if __name__ == '__main__':
	feed = RssFeed(feed_url='http://mashable.com/feed')
	for entry in feed.read():
		print entry.title
