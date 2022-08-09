import logging
import os
import sys

import django


def load_django():
    # Allow Scrapy to use Django
    sys.path.append(f'{os.path.dirname(os.path.realpath(__file__))}/../../backend')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'
    django.setup()


def enable_debug():
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
