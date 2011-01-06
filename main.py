import sys
import time
import random
import simplejson
from twibots import tb, sources, filters, channels
from twibots import tools

tools.enable_debug()
access_tokens = tools.file_auth()

twitter = tools.twitter_auth(access_tokens)
print "Input text to tweet: ",
text = sys.stdin.readline().strip()
writable = tb.Writable()
writable.output = text
writable.actions = ['default']
twitter.write(writable)

exit()
	
def rss():
	print "And now an RSS feed, input some RSS feed URLs and type 'go' when you're ready."
	
	rss_sources = []
	while True:
		print "RSS URL: ",
		url = sys.stdin.readline().strip()
		if url != 'go':
			rss_sources.append(url)
		else:
			break
	
	print "Cool, gathering some info... Will tweet links with a 30 seconds interval."
	print "Note that we also use a few filters here: bitly, inline hashtags, tags2hashtags and the trim140 filter set at 100 length"
	
	twibot = tb.Twibot()
	twitter = twitter_auth()
	
	print "Great. We'll also let you define additional hashtags that will apply to inline only. Write them down, comma separated, no spaces"
	print "Additional hashtags: ",
	at = sys.stdin.readline().strip().split(',')
	
	twitter.filters.append(filters.NoRetweets())
	twitter.filters.append(filters.NoDuplicates())
	twitter.filters.append(filters.Bitly(username='kovshenin', api_key='R_9f3bde0c5e2d36a3e747490bb37a6d5d'))
	twitter.filters.append(filters.InlineHashtags(additional_tags=at))
	twitter.filters.append(filters.TagsToHashtags())
	twitter.filters.append(filters.Trim140(max_length=100))

	# Append our sources
	for url in rss_sources:
		twibot.sources.append(sources.RssFeed(feed_url=url, count=5))
		
	
	print "We'll let you search a keyword and follow users tweeting it"
	print "Keyword: ",
	
	kw = sys.stdin.readline().strip()
	
	# Let's also run a Twitter search and follow some users
	search = sources.TwitterSearch(twitter, q=kw, count=2)
	search.actions = ['follow']
	
	twibot.sources.append(search)

	twibot.channels.append(twitter)
	while(True):
		try:
			for life in twibot.live():
				interval = random.randrange(60,300)
				print "Sleeping %s" % interval
				time.sleep(interval)
			else:
				interval = random.randrange(60,300)
				print "Sleeping %s" % interval
				time.sleep(interval)
		except KeyboardInterrupt:
			print "Quitting"
			exit()
		except:
			print "Some error occoured, skipping one life cycle"
		
	print "Done, exiting..."

def retweet():
	print "Search, retweet and follow, hmmm..."
	print "Input keyword: ",
	keyword = sys.stdin.readline().strip()
	print "Cool, we'll search that for you and send out a couple of retweets"
	
	twitter = channels.Twitter(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
	twitter.filters.append(filters.NoRetweets())
	
	search = sources.TwitterSearch(twitter, q=keyword, count=2)
	search.actions = ['retweet']

	twibot = tb.Twibot()
	twibot.sources.append(search)
	twibot.channels.append(twitter)

	while(True):
		for life in twibot.live():
			time.sleep(5)
		
	print "Done, exiting..."
