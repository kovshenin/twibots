import sys
import time
import random
import simplejson
from twibots import tb, sources, filters, channels
from twibots import tools

# Enable the --debug key.
tools.enable_debug()

# Enable the --auth "authfile.auth" key and read values.
access_tokens = tools.file_auth()

# Try the access values, create a twitter object. If access credentials
# are invalid, this will take you through the OAuth registration
# process and ask to save tokens to file at the end.
twitter = tools.twitter_auth(access_tokens)

# Let's get some input text from the user
print "Input text to tweet: ",
text = sys.stdin.readline().strip()

# Create and fill in a writable
writable = tb.Writable()
writable.output = text
writable.actions = ['tweet']

# Write
twitter.write(writable)
