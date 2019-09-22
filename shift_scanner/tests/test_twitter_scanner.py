 #-*- coding: utf-8 -*-

import unittest
from unittest import mock
#from shift_scanner.scanners.twitter import Twitter
#
#
#@mock.patch('shift_scanner.scanners.twitter.twitter')
#class TwitterScannerUnitTests(unittest.TestCase):
#    MOCK_SHIFT_CODE = 'AAAAA-11111-BBBBB-22222-CCCCC'
#    def test_when_set_of_tweets_contain_shift_codes_the_scanner_returns_them(self, mock_twitter):
#        mock_tweet = mock.Mock() # Based on twitter.Api>GetUserTimeLine objects
#        mock_tweet.text = "This contains a shift code: {}".format(self.MOCK_SHIFT_CODE)
#
#        mock_tweets = [mock_tweet]
#        mock_twitter.Api.GetUserTimeLine.return_value = mock_tweets
#
#        twitter_scanner = Twitter()
#        results = twitter_scanner.scan()
#        self.assertEqual(mock_tweets, results)
