#-*- coding: utf-8 -*-

import re

SHIFT_CODE_PATTERN = re.compile('[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}')


def contains_shift_code(text, *args, **kwargs):
    return SHIFT_CODE_PATTERN.findall(text)
