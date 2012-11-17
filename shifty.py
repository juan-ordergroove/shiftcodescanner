import codecs, logging, os, re, smtplib, string, simplejson, twitter, traceback
from datetime import *
from types import *

# Script & Logging configurations
dir_name = os.path.dirname(__file__)
config_file = open(os.path.join(dir_name, '../shift.config'))
shift_config = simplejson.loads(config_file.read())
config_file.close()

logging.basicConfig(filename='/var/log/shiftscanner/scan.log'
                    , format='%(asctime)s %(message)s'
                    , datefmt='%m/%d/%Y %I:%M:%S %p'
                    , level=logging.INFO)

def send_mail(from_addrs, to, subject, body):
    msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                    from_addrs,
                    string.join(to, ","),
                    subject,
                    datetime.now(), body)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo() # for tls add this line
    smtp.starttls() # for tls add this line
    smtp.ehlo() # for tls add this line
    smtp.login(from_addrs, shift_config.get('g_p'))
    smtp.sendmail(from_addrs, to, msg)
    smtp.quit()
    
def write_codes(codes):
    logging.info('writing codes...')
    fout = codecs.open('codes.log', 'w', 'utf-8')
    fout.write(codes)
    fout.close()
    
    logging.info('emailing codes...')
    send_mail(shift_config.get('from_addrs')
            , shift_config.get('mailing_list')
            , 'New SHIFT codes posted'
            , codes
            )

def scan_for_codes():
    codes = ''
    past_codes = False
    
    two_hours_ago = datetime.utcnow() + timedelta(hours=-2)
    api = twitter.Api(consumer_key=shift_config.get('c_k')
            , consumer_secret=shift_config.get('c_s')
            , access_token_key=shift_config.get('at_k')
            , access_token_secret=shift_config.get('at_s')
            )

    logging.info('scanning users...')
    for user in shift_config.get('scan_users'):
    	timeline = api.GetUserTimeline(user)
    	for tweet in timeline:
            created = datetime.strptime(tweet.created_at, '%a %b %d %H:%M:%S +0000 %Y')
            if two_hours_ago > created: continue

            m = re.search('.*X360.*[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}', tweet.text)
            if m and m.group(0): codes += tweet.text
    
    if codes:
        try:
            f = codecs.open('codes.log', 'r', 'utf-8')
            past_codes = f.read()
            f.close()
        except:
            logging.info(traceback.format_exc())
            msg = {'codes': codes, 'traceback': traceback.format_exc() }
            send_mail('juanny.gee@gmail.com'
                    , ['juanny.gee@gmail.com']
                    , 'code scan failure'
                    , simplejson.dumps(msg)
                    )
        
        if past_codes == codes: logging.info("these codes have already been delivered")
        else: write_codes(codes)
    else:
        logging.info('no new codes')

if __name__ == '__main__':
    scan_for_codes()
