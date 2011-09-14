#!/usr/bin/python

"""
	Twibots Retweet Example
	
	$ python retweet.py --retweet-id tweet_id --auth authfile.auth	
	
"""
import logging
import sys
import time
import random
import simplejson
from twibots import tb, sources, filters, channels
from twibots import tools

# Enable --debug argument
tools.enable_debug(log_filename='retweet.log')

# Enable --auth file.auth argument
access_tokens = tools.file_auth()

# Gather --id tweet_id argument
if '--retweet-id' in sys.argv:
	retweet_id = sys.argv[sys.argv.index('--retweet-id') + 1]
	logging.debug("Retweet id: %s" % retweet_id)

# Initialize the twitter channel using the access_tokens from file_auth().
twitter = tools.twitter_auth(access_tokens)

writable = tb.Writable()
writable.tweet_id = retweet_id
writable.actions = ['retweet']
twitter.write(writable)