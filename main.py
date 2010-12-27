class Twibot():
	actions = []
	filters = []
	channels = []
	
	def __init__(self, name=None):
		self.name = None
		pass
		
	def work(self):
		pass
		
	def rest(self):
		pass
	
class Action():
	
	def work(self):
		pass
	
class Filter():
	
	def filter(self):
		pass

class Channel():
	
	def write(self, text):
		pass
		
	def read(self, *args, **kwargs):
		pass

# Self-test code
if __name__ == '__main__':
	twibot = Twibot()
	rss = Action()
	regex = Filter()
	twitter = Channel()
	
	twibot.actions.append(rss)
	twibot.filters.append(regex)
	twibot.channels.append(twitter)
