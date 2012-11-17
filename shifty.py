import codecs, logging, os, re, smtplib, string, simplejson, twitter, traceback
from datetime import *
from types import *

logging.basicConfig(filename='/tmp/twitter_shift_code_scanner.log'
                    , format='%(asctime)s %(message)s'
                    , datefmt='%m/%d/%Y %I:%M:%S %p'
                    , level=logging.INFO)

def write_codes(codes):
    logging.info('writing codes...')
    fout = codecs.open('codes.log', 'w', 'utf-8')
    fout.write(codes)
    fout.close()
    
    logging.info('emailing codes...')
    p = open(os.path.join(dir_name, '../g.p')).read()
    from_addrs = 'juanny.gee@gmail.com'
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                    from_addrs,
                    string.join(mailing_list, ","),
                    'New SHIFT codes posted',
                    datetime.now(), codes)
    smtp.ehlo() # for tls add this line
    smtp.starttls() # for tls add this line
    smtp.ehlo() # for tls add this line
    smtp.login(from_addrs, p)
    smtp.sendmail(from_addrs, mailing_list, msg)
    smtp.quit()

dir_name = os.path.dirname(__file__)
c_k = open(os.path.join(dir_name, '../c.k')).read()
c_s = open(os.path.join(dir_name, '../c.s')).read()
a_t_k = open(os.path.join(dir_name, '../a_t.k')).read()
a_t_s = open(os.path.join(dir_name, '../a_t.s')).read()
mailing_list = simplejson.loads(open(os.path.join(dir_name, '../mailing_list.json')).read())

api = twitter.Api(consumer_key=c_k, consumer_secret=c_s, access_token_key=a_t_k, access_token_secret=a_t_s)
users = ['DuvalMagic', 'gearboxsoftware']
two_hours_ago = datetime.utcnow() + timedelta(hours=-2)
codes = ''

logging.info('scanning users...')
for user in users:
	timeline = api.GetUserTimeline(user)
	for tweet in timeline:
		created = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S +0000 %Y')
		if two_hours_ago > created: continue

		m = re.search('.*X360.*[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}', tweet.text)
		if m and m.group(0): codes += tweet.text

try:
    if codes:
        f = codecs.open('codes.log', 'r', 'utf-8')
        past_codes = f.read()

        if past_codes == codes: logging.info("these codes have already been delivered")
        else: write_codes(codes)
        f.close()
    else:
        logging.info('no new codes')
        pass
except:
    write_codes(codes)
