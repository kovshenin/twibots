#!/usr/bin/python

"""
	Twibots Twitter Authentication File Generator
	
	Use this script to create .auth files which could later be used with
	the --auth "filename" parameter. The launched script guides you through
	the OAuth registration process at Twitter, asks for the PIN provided
	by Twitter and saves the tokens to the given filename.
	
	$ python auth.py
	
	Warning! Don't share your .auth files as hackers could use them to
	do stuff with your Twitter account.
"""
import sys
import time
import random
import simplejson
from twibots import tb, sources, filters, channels
from twibots import tools

# Enable the --debug key.
tools.enable_debug()

# Start the registration process.
tools.twitter_register()
