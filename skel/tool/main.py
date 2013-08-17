#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import sys
import codecs
import requests
import requests_cache
from collections import OrderedDict
from cStringIO import StringIO
import datetime
import scraperwiki

BASE_URL = 'http://www.google.com'
UNIQUE_KEYS = []


def main():
    install_cache()

    fobj = download_url(BASE_URL)
    for row in process(fobj):
        scraperwiki.sqlite.save(
            unique_keys=UNIQUE_KEYS,
            data=row)
    update_status()


def update_status():
    status_text = 'Latest entry: {}'.format(
        get_most_recent_record('swdata', 'date'))
    print(status_text)

    scraperwiki.status('ok', status_text)


def install_cache():
    requests_cache.install_cache(
        expire_after=(12 * 60 * 60),
        allowable_methods=('GET',))


def download_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return StringIO(response.content)


def get_most_recent_record(table_name, column):
    result = scraperwiki.sql.select(
        "MAX({1}) AS most_recent FROM {0} LIMIT 1".format(table_name, column))
    return result[0]['most_recent']


def process(f):
    """
    Take a file-like object and yield OrderedDicts.
    """
    row = OrderedDict([
        ('date', datetime.datetime.now()),
        ('demo_column_a', True),
        ('demo_column_b', 7.0)])
    yield row

if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    main()
