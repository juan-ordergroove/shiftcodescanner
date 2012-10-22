import twitter, re
from datetime import *

api = twitter.Api(consumer_key='', consumer_secret='', access_token_key='', access_token_secret='')
users = ['DuvalMagic', 'gearboxsoftware']
yesterday = (datetime.now() - timedelta(1)).date()

for user in users:
	timeline = api.GetUserTimeline(user)
	for tweet in timeline:
		created = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S +0000 %Y').date()
		print created, yesterday, created < yesterday
		if created < yesterday: continue
		
		m = re.search('X360: [A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}', tweet.text)
		if m and m.group(0): print "Found!", m.group(0)