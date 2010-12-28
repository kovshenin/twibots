import core as tb
import extras.twitter as twitter
import urllib2

CONSUMER_KEY = 'cKlpH5jndEfrnhBQrrp8w'
CONSUMER_SECRET = 'reeYtKhTY7LRTwzXE5tmFrxwkD4lLVY9FgxrY5KFsE'

class TwitterInvalidVerifier(): pass
class TwitterUnauthorized(): pass
class TwitterPermalinkTooLong(): pass

class Twitter(tb.Channel):
	def __init__(self, consumer_key, consumer_secret, access_tokens=None, max_length=140):
		self.max_length = max_length
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.access_tokens = access_tokens
		
		if not access_tokens:
			self.api = None
			self.authenticated = False
		else:
			self.authenticated = True
			self.api = twitter.OAuthApi(self.consumer_key, self.consumer_secret, self.access_tokens['oauth_token'], self.access_tokens['oauth_token_secret'])
			self.verify_credentials()

	# Verify the credentials, assuming access tokens were supplied in the class
	# constructor.
	def verify_credentials(self):
		try:
			self.api('account/verify_credentials')
		except urllib2.HTTPError:
			raise TwitterUnauthorized

	# Initiate OAuth registration
	def register(self):
		self.api = twitter.OAuthApi(self.consumer_key, self.consumer_secret)
		credentials = self.api.getRequestToken()
		self.request_tokens = credentials
		return self.api.getAuthorizationURL(credentials)
	
	# Continue OAuth registration
	def validate(self, oauth_verifier):
		self.api = twitter.OAuthApi(self.consumer_key, self.consumer_secret)
		request_tokens = {'oauth_token': self.request_tokens['oauth_token'], 'oauth_token_secret': self.request_tokens['oauth_token_secret']}
		
		try:
			credentials = self.api.getAccessToken(request_tokens, oauth_verifier)
		except ValueError:
			raise TwitterInvalidVerifier

		self.access_tokens = {'oauth_token': credentials['oauth_token'], 'oauth_token_secret': credentials['oauth_token_secret']}
		self.screen_name = credentials['screen_name']
		self.api = twitter.OAuthApi(self.consumer_key, self.consumer_secret, self.access_tokens['oauth_token'], self.access_tokens['oauth_token_secret'])
		self.authenticated = True
		del self.request_tokens

	def write(self, writable):
		writable = self.filter(writable) # pass thru filters (see tb.Channel inheritance)
		tags = []
		for tag in writable.tags:
			tags.append('#%s' % tag)

		while True:
			# Loop while our length is not less or equal to max length
			if self.length(writable.title, writable.permalink, tags) <= self.max_length:
				break
			
			# Do we have any hashtags left?
			if len(tags):
				tags = tags[:-1]#.remove(len(writable.tags))
				continue
				
			# Start shoreting the title (by removing single words)
			if len(writable.title):
				writable.title = ' '.join(writable.title.split()[:-1])
				print 'stripping some title'
				continue
				
			# Permalink too long
			raise TwitterPermalinkTooLong

		final = ("%s %s %s" % (writable.title, writable.permalink, ' '.join(tags))).strip()
		print "Tweeting (%s): %s" % (len(final), final)
		#self.api.post('statuses/update', {'status': writable.title})
		
	def length(self, title, permalink, tags=[]):
		s = "%s %s %s" % (title, permalink, ' '.join(tags))
		return len(s.strip())

# Self-test code.
if __name__ == '__main__':
	import sys
	
	ch = Twitter(CONSUMER_KEY, CONSUMER_SECRET)
	"""
	print "Register here: %s" % ch.register()
	print "Verification code: ",
	oauth_verifier = sys.stdin.readline()
	ch.validate(oauth_verifier.strip())
		
	print "You are now verified: @%s" % ch.screen_name
	"""
	ch.max_length = 120
	writable = tb.Writable(
		title='Lorem Ipsum Dolor sit Amet',
		excerpt='excerpt',
		content='content',
		permalink='http://google.com',
		tags=['lorem', 'ipsum']
	)
	
	ch.write(writable)
