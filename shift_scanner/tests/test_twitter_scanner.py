 #-*- coding: utf-8 -*-

import unittest
from unittest import mock
from twitter.models import Status

from shift_scanner.scanners.twitter import Twitter


@mock.patch('shift_scanner.scanners.twitter.twitter')
class TwitterScannerUnitTests(unittest.TestCase):
    MOCK_SHIFT_CODE = 'AAAAA-11111-BBBBB-22222-CCCCC'

    def setUp(self):
        self.mock_tweets = [Status.NewFromJsonDict({"text": c}) for c in ['a', 'b', 'c']]

    def test_twitter_scanner_returns_an_empty_list_when_no_tweets_contain_shift_codes(self, mock_twitter):
        mock_twitter.Api.return_value.GetUserTimeLine.return_value = self.mock_tweets

        twitter_scanner = Twitter()
        self.assertEqual([], twitter_scanner.filter())

    def test_twitter_scanner_returns_a_list_of_tweets_that_contain_shift_codes(self, mock_twitter):
        tweet_with_shift_code = Status.NewFromJsonDict({
            "text": "There's a shift code here! {}".format(self.MOCK_SHIFT_CODE)
        })
        self.mock_tweets.append(tweet_with_shift_code)

        twitter_scanner = Twitter()
        mock_twitter.Api.return_value.GetUserTimeLine.return_value = self.mock_tweets
        self.assertEqual([tweet_with_shift_code], twitter_scanner.filter())
