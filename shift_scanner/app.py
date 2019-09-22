#-*- coding:utf-8 -*-

import requests

from shift_scanner import scanners
from shift_scanner.settings import SETTINGS


class App(object):
    def __init__(self):
        self._twitter_scanner = scanners.Twitter()

    def run(self):
        res = self._twitter_scanner.filter()
        if res:
            data = {'content': "New SHIFT code found! {}".format(res)}
            requests.post(SETTINGS['discord']['webhook'], data=data)


if __name__ == '__main__':
    app = App()
    app.run()
