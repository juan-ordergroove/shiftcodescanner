import codecs, logging, os, re, smtplib, string, simplejson, twitter, traceback
from datetime import *
from types import *

# Script & Logging configurations
dir_name = os.path.dirname(__file__)
shift_config = simplejson.loads(open(os.path.join(dir_name, '../shift.config')).read())
logging.basicConfig(filename='/var/log/shiftscanner/scan.log'
                    , format='%(asctime)s %(message)s'
                    , datefmt='%m/%d/%Y %I:%M:%S %p'
                    , level=logging.INFO)

def write_codes(codes):
    logging.info('writing codes...')
    fout = codecs.open('codes.log', 'w', 'utf-8')
    fout.write(codes)
    fout.close()
    
    logging.info('emailing codes...')
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                    shift_config.get('from_addrs'),
                    string.join(shift_config.get('mailing_list'), ","),
                    'New SHIFT codes posted',
                    datetime.now(), codes)
    smtp.ehlo() # for tls add this line
    smtp.starttls() # for tls add this line
    smtp.ehlo() # for tls add this line
    smtp.login(shift_config.get('from_addrs'), shift_config.get('g_p'))
    smtp.sendmail(shift_config.get('from_addrs'), shift_config.get('mailing_list'), msg)
    smtp.quit()

def scan_for_codes():
    api = twitter.Api(consumer_key=shift_config.get('c_k')
            , consumer_secret=shift_config.get('c_s')
            , access_token_key=shift_config.get('at_k')
            , access_token_secret=shift_config.get('at_s')
            )
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

if __name__ == '__main__':
    scan_for_codes()
