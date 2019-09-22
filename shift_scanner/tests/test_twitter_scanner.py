 #-*- coding: utf-8 -*-

import datetime
import unittest
from unittest import mock

from twitter.models import Status
from shift_scanner.scanners.twitter import Twitter


@mock.patch('shift_scanner.scanners.twitter.twitter')
class TwitterScannerUnitTests(unittest.TestCase):
    DATE_FMT ='%a %b %d %H:%M:%S +0000 %Y' 
    MOCK_SHIFT_CODE = 'AAAAA-11111-BBBBB-22222-CCCCC'

    def setUp(self):
        self.created_at_now = datetime.datetime.utcnow().strftime(self.DATE_FMT)
        self.mock_tweets = [Status.NewFromJsonDict({
            "text": c,
            "created_at": self.created_at_now
        }) for i, c in enumerate(['a', 'b', 'c'])]

    def test_twitter_scanner_returns_an_empty_list_when_no_tweets_contain_shift_codes(self, mock_twitter):
        mock_twitter.Api.return_value.GetUserTimeLine.return_value = self.mock_tweets

        twitter_scanner = Twitter()
        self.assertEqual([], twitter_scanner.filter())

    def test_tweets_older_than_two_hours_are_ignored(self, mock_twitter):
        two_hours_ago = datetime.datetime.utcnow() - datetime.timedelta(hours=2)
        old_tweet_with_shift_code = Status.NewFromJsonDict({
            "text": "There's a shift code here! {}".format(self.MOCK_SHIFT_CODE),
            "created_at": two_hours_ago.strftime(self.DATE_FMT)
        })
        self.mock_tweets.append(old_tweet_with_shift_code)

        twitter_scanner = Twitter()
        mock_twitter.Api.return_value.GetUserTimeLine.return_value = self.mock_tweets
        self.assertEqual([], twitter_scanner.filter())

    def test_twitter_scanner_returns_a_list_of_links_to_tweets_that_contain_shift_codes(self, mock_twitter):
        tweet_with_shift_code = Status.NewFromJsonDict({
            "id": 1000,
            "user": {"screen_name": "screenname"},
            "text": "There's a shift code here! {}".format(self.MOCK_SHIFT_CODE),
            "created_at": self.created_at_now
        })
        self.mock_tweets.append(tweet_with_shift_code)

        twitter_scanner = Twitter()
        mock_twitter.Api.return_value.GetUserTimeLine.return_value = self.mock_tweets
        expected_url = 'https://twitter.com/{}/status/{}'.format(
            tweet_with_shift_code.user.screen_name,
            tweet_with_shift_code.id
        )
        self.assertEqual([expected_url], twitter_scanner.filter())
