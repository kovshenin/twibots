import core as tb
import extras.feedparser as feedparser

class RssFeed(tb.Source):
	def __init__(self, feed_url=''):
		self.feed_url = feed_url
	
	def read(self):
		feed = feedparser.parse(self.feed_url)
		for item in feed['entries']:
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
	feed = RssFeed(feed_url='http://kovshenin.com/feed')
	for entry in feed.read():
		print entry
