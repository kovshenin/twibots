import sys
import time
import random
import simplejson
from twibots import tb, sources, filters, channels

# Remove this line if you actually wanna tweet
if '--debug' in sys.argv:
	tb.Channel.fake = True
	print "Running in Debug mode"
	print
	
access_tokens = None
if '--auth' in sys.argv:
	f = sys.argv[sys.argv.index('--auth')+1]
	print "Using authentication file: %s" % f
	try:
		auth = file(f)
		access_tokens = simplejson.load(auth)
		auth.close()
	except:
		access_tokens = None
		print "Authentication failed"

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

def twitter_auth(try_auth_file=True):
	
	if try_auth_file:
		global access_tokens
		if access_tokens:
			twitter = channels.Twitter(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_tokens=access_tokens)
			if twitter.verify_credentials():
				print "Auth file accepted, proceeding"
				return twitter
				
			else:
				print "Auth file invalid, going manual"
	
	if tb.Channel.fake:
		return channels.Twitter(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)

	twitter = channels.Twitter(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
	print "Register here: %s" % twitter.register()
	print "Verification code: ",
	oauth_verifier = sys.stdin.readline()
	twitter.validate(oauth_verifier.strip())
	print "You are now verified: @%s" % twitter.screen_name
	print "Would you like to save your tokens? (yes/no): ",
	choice = sys.stdin.readline().strip()
	
	if choice == 'yes':
		print "Input filename: ",
		filename = sys.stdin.readline().strip()
		f = file(filename, 'w')
		simplejson.dump(twitter.access_tokens, f)
		f.close()
	
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
	writable.actions = ['default']
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
