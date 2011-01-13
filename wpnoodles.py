#!/usr/bin/python

"""
	Twibots @wpnoodles Example
	
"""
import logging
import sys
import time
import random
import simplejson
from twibots import tb, sources, filters, channels
from twibots import tools

# Enable --debug argument
tools.enable_debug(log_filename='wpnoodles.log')

# Enable --auth file.auth argument
access_tokens = tools.file_auth()

# Initialize the twitter channel using the access_tokens from file_auth().
twitter = tools.twitter_auth(access_tokens)

class WordPressPlugins(tb.Source):
	"""
		Require: pyquery
	"""
	def __init__(self, prefix="New #WordPress Plugin:"):
		self.revision = 0
		self.prefix = prefix
		self.cache = []
		
	def cache_all(self):
		"""
			Use this method to cache all the plugins first.
		"""
		for smth in self.read(cache_all=True):
			pass

	def read(self, cache_all=False):
		import urllib
		from pyquery import PyQuery as pq
		
		logging.debug("Reading WordPress Plugins Subversion.")
		html = urllib.urlopen('http://svn.wp-plugins.org/').read()
		doc = pq(html)
		
		# Cache by Subversion revision
		revision_text = doc('h2').text().lower()
		revision = int(revision_text[revision_text.find('revision ') + len('revision '):revision_text.find(':')])

		if self.revision >= revision:
			raise StopIteration

		self.revision = revision
		
		# Read all the links on the page
		plugins_t = doc('li a')
		plugins = []
		for plugin in plugins_t:
			plugins.append(plugin.text.strip('/'))

		del plugins_t
		del doc
		del html
		
		if cache_all:
			logging.debug("Caching %s entries." % len(plugins))
			self.cache = plugins
			raise StopIteration
		
		logging.debug("Cycling through plugins.")
		for plugin in plugins:
			if plugin in self.cache:
				continue
				
			readme = urllib.urlopen('http://svn.wp-plugins.org/%s/trunk/readme.txt' % plugin)
			line = readme.readline().replace('===', '').strip()
			readme.close()

			# Don't cache plugins that don't have a readme file yet, they might
			# get it in the future.
			if line.lower().startswith('<!doctype'):
				logging.debug("Found a plugin with no readme, skipping")
				continue

			if line.lower() == 'plugin name':
				logging.debug("Found a plugin named Plugin Name, skipping")
				continue

			logging.debug("Seems like a valid plugin, processing.")
			self.cache.append(plugin)
			
			plugin_slug = plugin
			plugin_name = line
			plugin_url = 'http://wordpress.org/extend/plugins/%s/' % plugin_slug
				
			writable = tb.Writable(
				title=self.prefix + " %s" % plugin_name,
				permalink=plugin_url
			)

			yield writable

# Initialize the WordPress plugins source.		
wp = WordPressPlugins()

# Create our robot.
twibot = tb.Twibot()

# Add a few filters to our channel.
# Used for shortening links, please don't abuse my bit.ly credentials.
twitter.filters.append(filters.Bitly(username='kovshenin', api_key='R_9f3bde0c5e2d36a3e747490bb37a6d5d'))

# Transform RSS feed tags into hashtags (appended to the end of tweets).
twitter.filters.append(filters.TagsToHashtags())

# Trim our tweets to 100 characters.
twitter.filters.append(filters.Trim140(max_length=100))

# So that we really tweet only *new* plugins.
logging.debug("Caching WordPress plugins entries.")
wp.cache_all()

# Append our source
twibot.sources.append(wp)

# Let's also run a Twitter search and follow some users
search = sources.TwitterSearch(twitter, q='#wordpress -RT -via', count=2)
search.actions = ['follow']

# Append the search source.
twibot.sources.append(search)

# Append the channel.
twibot.channels.append(twitter)

# On-going.
logging.debug("WP Noodles now alive!")
while(True):
	try:
		for life in twibot.live():
			interval = random.randrange(60,300)
			logging.debug("Sleeping %s" % interval)
			time.sleep(interval)
		else:
			interval = random.randrange(300,600)
			logging.debug("Sleeping %s" % interval)
			time.sleep(interval)
	except KeyboardInterrupt:
		exit()
	except Exception, e:
		logging.debug("Some error occoured, skipping one life cycle: %s" % e)
