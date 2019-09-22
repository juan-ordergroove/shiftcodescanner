#-*- coding: utf-8 -*-

import unittest

from shift_scanner.matcher import ShiftCodeMatcher

class ShiftCodeMatcherUnitTest(unittest.TestCase):
    def setUp(self):
        self.matcher = ShiftCodeMatcher()

    def test_a_string_that_does_not_contain_a_shift_code_return_false(self):
        self.assertFalse(self.matcher.contains_shift_code("This does not contain a shift code"))
