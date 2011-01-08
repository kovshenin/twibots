#!/usr/bin/python

import sys
import time
import random
import simplejson
from twibots import tb, sources, filters, channels
from twibots import tools

tb.Channel.fake = True
twibot = tb.Twibot()

tools.enable_debug()
access_tokens = tools.file_auth()

twitter = tools.twitter_auth(access_tokens)

rss = sources.RssFeed(feed_url='http://www.google.com/reader/public/atom/user/08886841141873836783/state/com.google/broadcast', count=10)

twitter.filters.append(filters.NoRetweets())
twitter.filters.append(filters.NoDuplicates())
twitter.filters.append(filters.Bitly(username='kovshenin', api_key='R_9f3bde0c5e2d36a3e747490bb37a6d5d'))
twitter.filters.append(filters.InlineHashtags())
twitter.filters.append(filters.TagsToHashtags())
twitter.filters.append(filters.YouTubeEmbed())
twitter.filters.append(filters.Trim140(max_length=100))

twibot.sources.append(rss)
twibot.channels.append(twitter)

for life in twibot.live():
	pass
