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

account = twitter.api('account/verify_credentials')
account_followers = account['followers_count']
account_friends = account['friends_count']

followers = []
next_cursor = -1
print "Gathering your followers, this will take approximately %s second(s)." % (str(round(account_followers/5000.0 * 4 + 1)))
while next_cursor:
	followers_chunk = twitter.api.get('followers/ids', {'cursor': next_cursor})
	followers += followers_chunk['ids']
	next_cursor = followers_chunk['next_cursor']
	time.sleep(2)
	
print "You've got %s followers" % len(followers)
print "Gathering your friends, 100 at a time"

non_followers = 0
total_friends = 0
unfollowed = []
unfollowed_count = 0
next_cursor = -1
while next_cursor:
	friends = twitter.api.get('statuses/friends', {'cursor': next_cursor})
	next_cursor = friends['next_cursor']
	friends = friends['users']
	
	for friend in friends:
		total_friends += 1
		if not friend['id'] in followers:
			non_followers += 1
			print "(%s/%s) " % (total_friends, account_friends),
			#print "%s (@%s) is not following you, unfollow? (y/n): " % (friend['name'], friend['screen_name']),
			choice = 'y'#sys.stdin.readline().strip().lower()
			if choice.startswith('y'):
				unfollowed_count += 1
				unfollowed.append(friend['screen_name'])
				print "Unfollowing @%s" % friend['screen_name']
				try:
					twitter.api.post('friendships/destroy', {'screen_name': friend['screen_name']})
				except urllib2.HTTPError as e:
					print "HTTP Error: %s" % e
					
				time.sleep(5)

print "%s out of %s of your friends did not follow you back" % (non_followers, total_friends)
print "You have unfollowed %s of them" % len(unfollowed)

print "\n\n\nThank you for using this script, happy following!"
