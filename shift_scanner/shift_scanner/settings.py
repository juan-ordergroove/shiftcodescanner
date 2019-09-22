#-*- coding: utf-8 -*-

import os
import configparser


CFG_PATH = os.getenv("SHIFT_CODE_SCANNER_CFG_PATH", os.path.expanduser("~/shift_code_scanner.cfg"))
SETTINGS = configparser.ConfigParser()
SETTINGS.read(CFG_PATH)
