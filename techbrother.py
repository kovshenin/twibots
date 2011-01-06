"""
	Twibots @techbrother Example
	
	This is a sample to illustrate the work of @techbrother on Twitter, which
	is a robot that gathers some info from various RSS feeds and tweets them
	out with a random interval, kind of what Twitterfeed does.
	
	Use of filters are well illustrated in this example. Caching doesn't happen
	in a file, because we're assuming you'll run this as a background task.
	
	@techbrother also performs a Twitter search from time to time using
	some keywords, and follows the people tweeting those keywords.
	
	Use the following command to launch @techbrother, assuming you have a valid
	auth file (we won't provide you with @techbrother's actual .auth file, so
	use your own Twitter account).
	
	$ python techbrother.py --auth authfile.auth
	
	Press Ctrl+Z and type "bg" to force the task as background. Then find it using
	"ps aux | grep python" and kill it using the process id to stop tweeting.
	
	To debug use:
	
	$ python techbrother.py --auth authfile.auth --debug --fake
	
	This will generate a techbrother.log file with all the debug entries,
	and it will not use your Twitter account to actually tweet (fake).
"""
import logging
import sys
import time
import random
import simplejson
from twibots import tb, sources, filters, channels
from twibots import tools

# Enable --debug argument
tools.enable_debug(log_filename='techbrother.log')

# Enable --auth file.auth argument
access_tokens = tools.file_auth()

# Initialize the twitter channel using the access_tokens from file_auth().
twitter = tools.twitter_auth(access_tokens)

# Sources to round-robin.
rss_sources = [
	'http://mashable.com/feed',
	'http://techcrunch.com/feed',
	'http://kovshenin.com/feed',
	'http://www.google.com/reader/public/atom/user/08886841141873836783/state/com.google/broadcast', # This is an atom feed of my shared items on Google Reader
]

# Create our robot.
twibot = tb.Twibot()

# Add a few filters to our channel.
# Certain feeds can publish duplicate content, we use this filter to avoid tweeting it.
twitter.filters.append(filters.NoDuplicates())

# Used for shortening links, please don't abuse my bit.ly credentials.
twitter.filters.append(filters.Bitly(username='kovshenin', api_key='R_9f3bde0c5e2d36a3e747490bb37a6d5d'))

# Some feeds don't come with categories, thus we can provide a set of
# so called additional or possible tags that may be in the title. We
# hashtagify these and throw the rest away, so we won't be actually tweeting
# #apple with every tweet.
twitter.filters.append(filters.InlineHashtags(additional_tags=['wordpress', 'design', 'jquery', 'drupal', 'google', 'apple'])) 

# Transform RSS feed tags into hashtags (appended to the end of tweets).
twitter.filters.append(filters.TagsToHashtags())

# Trim our tweets to 100 characters.
twitter.filters.append(filters.Trim140(max_length=100))

# Append our sources, 5 items from each source. We'll read the current
# items in order to cache them inside the RssFeed objects, so that
# finally we tweet only new entries.
logging.debug("Reading RSS sources and caching initial data.")
for url in rss_sources:
	rss = sources.RssFeed(feed_url=url, count=5)
	for item in rss.read():
		pass

	twibot.sources.append(rss)

# Let's also run a Twitter search and follow some users
search = sources.TwitterSearch(twitter, q='#tech', count=2)
search.actions = ['follow']

# Append the search source.
twibot.sources.append(search)

# Append the channel.
twibot.channels.append(twitter)

# On-going.
logging.debug("Techbrother now alive!")
while(True):
	try:
		for life in twibot.live():
			interval = random.randrange(60,300)
			logging.debug("Sleeping %s" % interval)
			time.sleep(interval)

	except KeyboardInterrupt:
		exit()
	except:
		logging.error("Some error occoured, skipping one life cycle")
