from twibots import tb, sources, filters, channels

twibot = tb.Twibot()

twitter = channels.Twitter()
twitter.filters.append(filters.InlineHashtags())
twitter.filters.append(filters.Bitly(username='kovshenin', api_key='R_9f3bde0c5e2d36a3e747490bb37a6d5d'))

rss = sources.RssFeed(feed_url='http://kovshenin.com/feed')

twibot.sources.append(rss)
twibot.channels.append(twitter)

twibot.live()
