import sys
import shelve
import time
from twibots import tb, sources, filters, channels

CONSUMER_KEY = 'cKlpH5jndEfrnhBQrrp8w'
CONSUMER_SECRET = 'reeYtKhTY7LRTwzXE5tmFrxwkD4lLVY9FgxrY5KFsE'

config = shelve.open('config')
twibot = tb.Twibot()

#del config['twitter_auth']
#config.close()
#exit()

if 'twitter_auth' in config:
	access_tokens = config['twitter_auth']
	twitter = channels.Twitter(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_tokens=access_tokens)
else:
	twitter = channels.Twitter(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
	print "Register here: %s" % twitter.register()
	print "Verification code: ",
	oauth_verifier = sys.stdin.readline()
	twitter.validate(oauth_verifier.strip())
	print "You are now verified: @%s" % twitter.screen_name
	config['twitter_auth'] = twitter.access_tokens

#twitter = channels.Twitter(consumer_key='cKlpH5jndEfrnhBQrrp8w', consumer_secret='reeYtKhTY7LRTwzXE5tmFrxwkD4lLVY9FgxrY5KFsE')

twitter.filters.append(filters.Bitly(username='kovshenin', api_key='R_9f3bde0c5e2d36a3e747490bb37a6d5d'))
twitter.filters.append(filters.InlineHashtags())
twitter.filters.append(filters.TagsToHashtags())
twitter.filters.append(filters.Trim140(max_length=70))

rss = sources.RssFeed(feed_url='http://kovshenin.com/feed', count=10)

twibot.sources.append(rss)
twibot.channels.append(twitter)

for life in twibot.live():
	print "Twibot living, channel output: %s" % life
	print "Resting ...\n"
	time.sleep(1)
	twibot.rest()
	
config.close()
