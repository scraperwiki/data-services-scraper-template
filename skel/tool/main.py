#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import sys
import codecs
import datetime
import requests
import requests_cache
import scraperwiki
from collections import OrderedDict

BASE_URL = 'http://www.google.com'


def main():
    install_cache()

    html = download_url(BASE_URL)
    for row in process(html):
        scraperwiki.sqlite.save(unique_keys=[], data=row)

    scraperwiki.status('ok', 'Run was successful.')


def install_cache():
    requests_cache.install_cache(
        expire_after=(12 * 60 * 60),
        allowable_methods=('GET', 'POST'))


def download_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def process(html):
    row = OrderedDict([
        ('run_datetime', datetime.datetime.now()),
        ('demo_column_a', True),
        ('demo_column_b', 7.0)])
    yield row

if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    main()
