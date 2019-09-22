#-*- coding: utf-8 -*-

import unittest

from shift_scanner.matcher import ShiftCodeMatcher


class ShiftCodeMatcherUnitTest(unittest.TestCase):
    def test_when_a_string_does_not_contain_a_SHIFT_code_the_matcher_returns_false(self):
        self.assertFalse(
            ShiftCodeMatcher.contains_shift_code("This does not contain a shift code")
        )

    def test_when_a_string_contains_a_SHIFT_code_the_matcher_returns_true(self):
        self.assertTrue(
            ShiftCodeMatcher.contains_shift_code("This has a shift code: AAAAA-11111-BBBBB-22222-CCCCC")
        )
