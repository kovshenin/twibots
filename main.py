import sys
import time
import random
from twibots import tb, sources, filters, channels

# Remove this line if you actually wanna tweet
tb.Channel.fake = True

CONSUMER_KEY = 'Ai5tJWvg0UEnPNzOoDrP8A'
CONSUMER_SECRET = 'LAWbNw7ovHBHES6ymBLCWjx28oZT3wLRRB8PBV7sk'

print "Welcome to Twibots, please pick one of the options below"
print "1. Tweet hello world via Twibots"
print "2. Tweet any text of your input"
print "3. Tweet into two different Twitter accounts"
print "4. Tweet links from an RSS feed"
print "5. Search and retweet something"
print "0. Exit"
print
print "Choice: ",
choice = sys.stdin.readline().strip()
print

def twitter_auth():
	twitter = channels.Twitter(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
	print "Register here: %s" % twitter.register()
	print "Verification code: ",
	oauth_verifier = sys.stdin.readline()
	twitter.validate(oauth_verifier.strip())
	print "You are now verified: @%s" % twitter.screen_name
	
	return twitter

def hello_world():
	print "Welcome to Hello World!"
	twitter = twitter_auth()
	print "I will now tweet Hello World from your Twitter account"
	
	writable = tb.Writable()
	writable.output = "Hello World!"
	twitter.write(writable)
	
	print "Done, exiting..."

def input_text():
	print "Tweet anything you like, authenticate first"
	twitter = twitter_auth()
	print "Input text to tweet: ",
	text = sys.stdin.readline().strip()
	
	writable = tb.Writable()
	writable.output = text
	print "Tweeting: %s" % text
	twitter.write(writable)
	
	print "Done, exiting..."
	
def dual_account():
	print "Dual account, authenticate first account"
	twitter1 = twitter_auth()
	print "Cool, now the second one please"
	twitter2 = twitter_auth()
	print "Nice, so what would you like to tweet from both accounts?"
	print "Tweet: ",
	
	text = sys.stdin.readline().strip()
	writable = tb.Writable()
	writable.output = text
	
	print "Tweeting from first account"
	twitter1.write(writable)
	print "Tweeting from second account"
	twitter2.write(writable)
	
	print "Done, exiting..."
	
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
	
	twitter.filters.append(filters.Bitly(username='kovshenin', api_key='R_9f3bde0c5e2d36a3e747490bb37a6d5d'))
	twitter.filters.append(filters.InlineHashtags())
	twitter.filters.append(filters.TagsToHashtags())
	twitter.filters.append(filters.Trim140(max_length=100))

	# Let's make a list of a few sources
	#rss_sources = ["http://mashable.com/feed", "http://kovshenin.com/feed", "http://techcrunch.com/feed", "http://smashingmagazine.com/feed"]
	for url in rss_sources:
		twibot.sources.append(sources.RssFeed(feed_url=url, count=3))

	twibot.channels.append(twitter)
	
	while(True):
		for life in twibot.live():
			time.sleep(random.randrange(50,300))
		
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
	
options = {
	'1': hello_world,
	'2': input_text,
	'3': dual_account,
	'4': rss,
	'5': retweet,
	'0': exit
}

options[choice]()
exit()
