#!/usr/bin/python

"""
	Twibots PubSubHubBub Example
	
	This has to be used in pair with a subscriber (see HubBub definition). The
	subscriber, which can be a simple PHP or Python script running on a server
	that could be reached by a Hub, receives "pings" from the Hubs which means
	there's new content. At this stage you should fire this script:
	
	 $ cd /path/to/twibots && python hubbub.py --auth whatever.auth --cache whatever.cache
	 
	 Caching to file is used in this example since it's not an on-going daemon,
	 it exists after tweeting a couple of entries from the feed.
	 
	 If you don't have an .auth file, use the auth.py script to generate one.
"""
import sys
import time
import random
import simplejson
from twibots import tb, sources, filters, channels
from twibots import tools

# Enable the --debug key.
tools.enable_debug()

# Enable the --auth "authfile.auth" key and read values.
access_tokens = tools.file_auth()

# Try the access values, create a twitter object. If access credentials
# are invalid, this will take you through the OAuth registration
# process and ask to save tokens to file at the end.
twitter = tools.twitter_auth(access_tokens)

# Let's look for the --cache "file.cache" key in the command line args.
# If they exist we can load the cache data from the file, otherwise
# use it later to save the cache.
if '--cache' in sys.argv:
	cache_filename = sys.argv[sys.argv.index('--cache')+1]
	logging.debug("Using cache file: %s" % cache_filename)
	try:
		cache = file(cache_filename)
		cache_values = simplejson.load(cache)
		cache.close()
	except:
		cache_values = []
		logging.debug("Cache load failed (empty?)")

# Create the Twibot.
twibot = tb.Twibot()

# Create the NoDuplicates filter and load up the cache values.
nodups = filters.NoDuplicates()
nodups.cache = cache_values

# Append some filters including the no duplicates filter.
twitter.filters.append(nodups)
twitter.filters.append(filters.Bitly(username='kovshenin', api_key='R_9f3bde0c5e2d36a3e747490bb37a6d5d'))
twitter.filters.append(filters.InlineHashtags())
twitter.filters.append(filters.TagsToHashtags())
twitter.filters.append(filters.Trim140(max_length=100))

# Create an RSS feed source (Atom).
rss = sources.RssFeed(feed_url='http://www.google.com/reader/public/atom/user/08886841141873836783/state/com.google/broadcast', count=2)

# Append our sources and channels
twibot.sources.append(rss)
twibot.channels.append(twitter)

# Behold!
for life in twibot.live():
	pass

# Let's save the cache into the given file.
logging.debug("Saving cache..")
f = file(cache_filename, 'w')
simplejson.dump(nodups.cache, f)
f.close()
