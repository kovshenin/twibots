import sys
import time
from twibots import tb, sources, filters, channels

CONSUMER_KEY = 'cKlpH5jndEfrnhBQrrp8w'
CONSUMER_SECRET = 'reeYtKhTY7LRTwzXE5tmFrxwkD4lLVY9FgxrY5KFsE'

print "Welcome to Twibots, please pick one of the options below"
print "1. Tweet hello world via Twibots"
print "2. Tweet any text of your input"
print "3. Tweet into two different Twitter accounts"
print "4. Tweet 3 links from an RSS feed"
print "5. Search and retweet something"
print "6. Exit"
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
	print "And now an RSS feed, input the URL to an RSS feed"
	print "RSS URL: ",
	
	url = sys.stdin.readline().strip()
	
	print "Cool, gathering some info... Will tweet 3 links with a 20 seconds interval."
	print "Note that we also use a few filters here: bitly, inline hashtags, tags2hashtags and the trim140 filter set at 100 length"
	
	twibot = tb.Twibot()
	twitter = twitter_auth()
	
	twitter.filters.append(filters.Bitly(username='kovshenin', api_key='R_9f3bde0c5e2d36a3e747490bb37a6d5d'))
	twitter.filters.append(filters.InlineHashtags())
	twitter.filters.append(filters.TagsToHashtags())
	twitter.filters.append(filters.Trim140(max_length=100))

	rss = sources.RssFeed(feed_url=url, count=3)
	
	twibot.sources.append(rss)
	twibot.channels.append(twitter)
	
	for life in twibot.live():
		print life
		time.sleep(20)
		
	print "Done, exiting..."

def retweet():
	print "Search, retweet and follow, hmmm..."
	print "Input keyword: ",
	keyword = sys.stdin.readline().strip()
	print "Cool, we'll search that for you and send out a couple of retweets"
	
	twitter = channels.Twitter(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
	search = sources.TwitterSearch(twitter, q=keyword, count=2)
	search.actions = ['retweet', 'follow']

	twibot = tb.Twibot()
	twibot.sources.append(search)
	twibot.channels.append(twitter)

	for life in twibot.live():
		print life
		
	print "Done, exiting..."
	
options = {
	'1': hello_world,
	'2': input_text,
	'3': dual_account,
	'4': rss,
	'5': retweet,
	'6': exit
}

options[choice]()
exit()
