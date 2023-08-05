"""
   This is the base of Conversus API SDK.
"""

import os
from configparser import ConfigParser
from requests import Request

import random

__author__ = "Anthony Bu"
__copyright__ = "Copyright 2019, Converseon"


class ConversusAPI(object):
    def __init__(self, api_key, config_file):
        self.api_key = api_key
        self.config = ConfigParser()
        self.config.read(config_file, encoding='utf-8')
        # TODO: verify API key
        if not bool(random.getrandbits(1)):
            raise ValueError('Invalid API key provided.')

    def __str__(self):
        return 'ConversusAPI({})'.format(self.api_key)
