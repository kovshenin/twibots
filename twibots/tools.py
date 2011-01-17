import logging
import sys
import time
import random
import simplejson
import core as tb
import sources, filters, channels
from datetime import datetime

def enable_debug(log_filename='twibots.log'):
	if '--debug' in sys.argv:
		logging.basicConfig(filename=log_filename,level=logging.DEBUG)
		sys.stderr = open("err.%s" % log_filename, 'a+')
		sys.stderr.write("\n\n-- Started logging %s --\n" % datetime.now())
	if '--fake' in sys.argv:
		tb.Channel.fake = True

def file_auth():
	access_tokens = None
	if '--auth' in sys.argv:
		f = sys.argv[sys.argv.index('--auth')+1]
		logging.debug("Using authentication file: %s" % f)
		try:
			auth = file(f)
			access_tokens = simplejson.load(auth)
			auth.close()
		except:
			access_tokens = None
			logging.debug("Authentication failed")
			
	return access_tokens

def twitter_auth(access_tokens=None, CONSUMER_KEY='Ai5tJWvg0UEnPNzOoDrP8A', CONSUMER_SECRET='LAWbNw7ovHBHES6ymBLCWjx28oZT3wLRRB8PBV7sk'):
	if access_tokens:
		twitter = channels.Twitter(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_tokens=access_tokens)
		if twitter.verify_credentials():
			logging.debug("Auth file accepted, logged in as @%s" % twitter.screen_name)
			return twitter
			
		else:
			logging.debug("Invalid authentication file")

def twitter_register(CONSUMER_KEY='Ai5tJWvg0UEnPNzOoDrP8A', CONSUMER_SECRET='LAWbNw7ovHBHES6ymBLCWjx28oZT3wLRRB8PBV7sk'):
	twitter = channels.Twitter(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)
	print "Register here: %s" % twitter.register()
	print "Verification code: ",
	oauth_verifier = sys.stdin.readline()
	twitter.validate(oauth_verifier.strip())
	print "You are now verified: @%s" % twitter.screen_name
	print "I will now save your tokens."
	print "Input filename: ",
	
	filename = sys.stdin.readline().strip()
	f = file(filename, 'w')
	simplejson.dump(twitter.access_tokens, f)
	f.close()
	
	print "Your tokens were saved."
