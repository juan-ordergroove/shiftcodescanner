#-*- coding: utf-8 -*-

import twitter
from shift_scanner.matcher import contains_shift_code


class Twitter(object):
    def __init__(self, *args, **kwargs):
        self._api = twitter.Api(
            consumer_key='',
            consumer_secret='',
            access_token_key='',
            access_token_secret=''
        )

    def filter(self, *args, **kwargs):
        tweets_with_shift_codes = []
        tweets = self._api.GetUserTimeLine(screen_name='dgShiftCodes')
        for tweet in tweets:
            if contains_shift_code(tweet.text):
                tweets_with_shift_codes.append(tweet)
        return tweets_with_shift_codes
