import sys
import time
import random
import simplejson
from twibots import tb, sources, filters, channels

log_file = file("log.txt", "a+")
sys.stdout = log_file

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
		print "Authentication failed!"
		
if '--cache' in sys.argv:
	cache_filename = sys.argv[sys.argv.index('--cache')+1]
	print "Using cache file: %s" % cache_filename
	try:
		cache = file(cache_filename)
		cache_values = simplejson.load(cache)
		cache.close()
	except:
		cache_values = []
		print "Cache load failed (empty?)"

CONSUMER_KEY = 'Ai5tJWvg0UEnPNzOoDrP8A'
CONSUMER_SECRET = 'LAWbNw7ovHBHES6ymBLCWjx28oZT3wLRRB8PBV7sk'

def twitter_auth(try_auth_file=True):
	if try_auth_file:
		global access_tokens
		if access_tokens:
			twitter = channels.Twitter(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_tokens=access_tokens)
			if twitter.verify_credentials():
				print "Auth file accepted, proceeding"
				return twitter
				
	print "Invalid authentication, exiting."
	exit()

twibot = tb.Twibot()
twitter = twitter_auth()
nodups = filters.NoDuplicates()

nodups.cache = cache_values

twitter.filters.append(nodups)
twitter.filters.append(filters.Bitly(username='kovshenin', api_key='R_9f3bde0c5e2d36a3e747490bb37a6d5d'))
twitter.filters.append(filters.InlineHashtags())
twitter.filters.append(filters.TagsToHashtags())
twitter.filters.append(filters.Trim140(max_length=100))

rss = sources.RssFeed(feed_url='http://www.google.com/reader/public/atom/user/08886841141873836783/state/com.google/broadcast', count=1)

# Append our sources
twibot.sources.append(rss)
twibot.channels.append(twitter)
for life in twibot.live():
	pass
	
print "Saving cache.."
f = file(cache_filename, 'w')
simplejson.dump(nodups.cache, f)
f.close()

print "Done, exiting..."
