#-*- coding: utf-8 -*-

import twitter

#from shift_scanner.scanners.base import ShiftScanner
#
#
#class Twitter(ShiftScanner):
#    def __init__(self, *args, **kwargs):
#        self._api = twitter.Api(
#            consumer_key='',
#            consumer_secret='',
#            access_token_key='',
#            access_token_secret=''
#        )
#
#    def _scan(self, *args, **kwargs):
#        # TODO: replace hardcoded screen name with list of screen names from CFG
#        tweets = self._api.GetUserTimeLine(screen_name='dgShiftCodes')
