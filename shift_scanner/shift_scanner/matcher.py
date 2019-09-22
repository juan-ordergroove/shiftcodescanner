#-*- coding: utf-8 -*-

import re


class ShiftCodeMatcher(object):
    SHIFT_CODE_PATTERN = re.compile('[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}')

    @classmethod
    def contains_shift_code(cls, text, *args, **kwargs):
        return cls.SHIFT_CODE_PATTERN.findall(text)
