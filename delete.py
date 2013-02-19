#!/usr/bin/python

"""
"""
import urllib2
import logging
import threading
import sys
import time
import random
import simplejson
from twibots import tb, sources, filters, channels
from twibots import tools

# Enable --auth file.auth argument
access_tokens = tools.file_auth()

# Initialize the twitter channel using the access_tokens from file_auth().
twitter = tools.twitter_auth(access_tokens)

#account = twitter.api('account/verify_credentials')
#account_followers = account['followers_count']
#account_friends = account['friends_count']
filename = None
if '--filename' in sys.argv:
	filename = sys.argv[sys.argv.index('--filename') + 1]

if not filename:
	print "Please provide an IDs filename with --filename <filename>"
	exit()

with open(filename) as f:
    content = f.readlines()

deleted = 0

for tweet_id in content:
	tweet_id = tweet_id.strip()
	if not tweet_id:
		continue

	print "Deleting %s... " % tweet_id,
	sys.stdout.flush()
	try:
		result = twitter.api.post('statuses/destroy/%s' % tweet_id)
		deleted += 1
		print "Yup"
	except:
		print "Nah"

print "Deleted %s tweets" % deleted