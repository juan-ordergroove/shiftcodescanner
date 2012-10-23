import twitter, re, os
from datetime import *

dir_name = os.path.dirname(__file__)
c_k = open(os.path.join(dir_name, '../c.k')).read()
c_s = open(os.path.join(dir_name, '../c.s')).read()
a_t_k = open(os.path.join(dir_name, '../a_t.k')).read()
a_t_s = open(os.path.join(dir_name, '../a_t.s')).read()

api = twitter.Api(consumer_key=c_k, consumer_secret=c_s, access_token_key=a_t_k, access_token_secret=a_t_s)
users = ['DuvalMagic', 'gearboxsoftware']
two_hours_ago = datetime.today() + timedelta(hours=-2)

for user in users:
	timeline = api.GetUserTimeline(user)
	for tweet in timeline:
		created = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S +0000 %Y')
		if two_hours_ago > created: continue

		m = re.search('X360: [A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}', tweet.text)
		if m and m.group(0): print "Found!", m.group(0)