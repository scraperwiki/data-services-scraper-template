#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import codecs
import datetime
import logging
import requests
import requests_cache
import sys

from collections import OrderedDict
from cStringIO import StringIO

import scraperwiki

BASE_URL = 'http://not.a.real.url'
INDEX_URL = BASE_URL + '/demo_index_page.html'

TEMPLATE_ROW = OrderedDict([
    ('date', None),      # None values are set later
    ('column_a', None),
    ('column_b', 9),     # this row is always the same
])

UNIQUE_KEYS = []


def main():
    logging.basicConfig(level=logging.DEBUG)
    install_cache()

    fobj = download_url(INDEX_URL)
    for row in process(fobj):
        scraperwiki.sqlite.save(
            unique_keys=UNIQUE_KEYS,
            data=row)
    update_status()


def update_status():
    status_text = 'Latest entry: {}'.format(
        get_most_recent_record('swdata', 'date'))
    logging.info(status_text)

    scraperwiki.status('ok', status_text)


def install_cache():
    requests_cache.install_cache(
        expire_after=(12 * 60 * 60),
        allowable_methods=('GET',))


def download_url(url):
    logging.debug("Download {}".format(url))
    response = requests.get(url)
    response.raise_for_status()
    return StringIO(response.content)


def get_most_recent_record(table_name, column):
    result = scraperwiki.sql.select(
        "MAX({1}) AS most_recent FROM {0} LIMIT 1".format(table_name, column))
    return result[0]['most_recent']


def process(f):
    """
    Take a file-like object and yield OrderedDicts to be inserted into db.
    """

    yield make_row(10)


def make_row(value):
    row = TEMPLATE_ROW.copy()
    row['date'] = datetime.datetime.now()
    row['column_a'] = value
    return

if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    main()
