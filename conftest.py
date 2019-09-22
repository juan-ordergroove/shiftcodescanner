#-*- coding: utf-8 -*-

import os

def pytest_configure():
    test_settings_path = '{}/test_settings.cfg'.format(os.path.dirname(os.path.abspath(__file__)))
    os.environ['SHIFT_CODE_SCANNER_CFG_PATH'] = test_settings_path
