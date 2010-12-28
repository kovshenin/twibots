import core as tb

class Twitter(tb.Channel):
	def write(self, writable):
		writable = self.filter(writable)
		print "Tweeting: %s %s" % (writable.title, writable.permalink)
