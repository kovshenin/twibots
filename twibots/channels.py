import core as tb
import extras.twitter as twitter
import urllib2

class TwitterInvalidVerifier(): pass
class TwitterUnauthorized(): pass
class TwitterNothingToTweet(): pass
class TwitterActionNotImplemented(): pass
	
class Twitter(tb.Channel):
	"""
		The main channel of all -- Twitter. This channel uses OAuth to authenticate
		with the Twitter API. Use the register() and validate() calls to walk through
		the registration process. Memorize the access_tokens returned by validate()
		and use them when initializing Twitter() next time to restore the session.
	"""
	def __init__(self, consumer_key, consumer_secret, access_tokens=None):
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.access_tokens = access_tokens
		
		if not access_tokens:
			self.api = twitter.OAuthApi(self.consumer_key, self.consumer_secret)
			self.authenticated = False
		else:
			self.authenticated = True
			self.api = twitter.OAuthApi(self.consumer_key, self.consumer_secret, self.access_tokens['oauth_token'], self.access_tokens['oauth_token_secret'])
			self.verify_credentials()

	def verify_credentials(self):
		"""
			Use this method to verify connection to the Twitter API at any given time.
			This method is also used when initializing Twitter() with an access_token
			to restore session.
		"""
		try:
			self.api('account/verify_credentials')
		except urllib2.HTTPError:
			raise TwitterUnauthorized

	def register(self):
		"""
			Initiate an OAuth registration session. Request tokens are stored and
			an authorization URL is returned. The registraion process assumes you're
			using PIN based OAuth.
		"""
		self.api = twitter.OAuthApi(self.consumer_key, self.consumer_secret)
		credentials = self.api.getRequestToken()
		self.request_tokens = credentials
		return self.api.getAuthorizationURL(credentials)
	
	def validate(self, oauth_verifier):
		"""
			Once the user receives a PIN code, use this method to validate it. In case
			of success, an access_tokens dictionary is returned. Store this dictionary
			and pass it on to the Twitter() init method next time to skip the authentication
			part.
		"""
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
		
		return self.access_tokens
		
	def write(self, writable):
		"""
			This is the method that actually tweets a Writable(). Note that
			all writables are passed through filters attached to the instance
			channel (inherited from tb.Channel).
		"""
		writable = self.filter(writable)
		actions = writable.actions
		for action in writable.actions:
			method = getattr(self, action, None)
			if method:
				method(writable)
			else:
				raise TwitterActionNotImplemented

	# Default action
	def default(self, writable):
		return self.tweet(writable)

	# Below is the list of all available actions for this channel.
	def tweet(self, writable):
		"""
			Writes a tweet invoking statuses/update call.
		"""
		try:
			if not writable.output:
				raise TwitterNothingToTweet
		except:
			raise TwitterNothingToTweet
		
		#self.api.post('statuses/update', {'status': writable.output.encode('utf-8')})
		print "Tweeting (%s): %s" % (len(writable.output), writable.output)

	def retweet(self, writable):
		"""
			Retweets a message in the writable, tweet_id has to be present
			in the writable.
		"""
		print "Retweeting: RT @%s %s" % (writable.author, writable.title)

	def list(self, writable):
		"""
			Lists a user to a specific list, list_name has to be present
			in the writable.
		"""
		print "Listing: @%s" % writable.author
		
	def follow(self, writable):
		"""
			Follows a user, author or author_id has to be present in
			the writable.
		"""
		print "Following: @%s" % writable.author
	
# Self-test code.
if __name__ == '__main__':
	import sys

	# Please don't abuse these
	CONSUMER_KEY = 'cKlpH5jndEfrnhBQrrp8w'
	CONSUMER_SECRET = 'reeYtKhTY7LRTwzXE5tmFrxwkD4lLVY9FgxrY5KFsE'
	
	ch = Twitter(CONSUMER_KEY, CONSUMER_SECRET)
	"""
	print "Register here: %s" % ch.register()
	print "Verification code: ",
	oauth_verifier = sys.stdin.readline()
	ch.validate(oauth_verifier.strip())
		
	print "You are now verified: @%s" % ch.screen_name
	"""
	
	writable = tb.Writable(
		title='Lorem Ipsum Dolor sit Amet',
		excerpt='excerpt',
		content='content',
		permalink='http://google.com',
		tags=['lorem', 'ipsum']
	)
	
	writable.output = "Hello world!"
	writable.author = 'kovshenin'
	
	writable.actions = ['tweet', 'retweet', 'follow']
	
	ch.write(writable)
