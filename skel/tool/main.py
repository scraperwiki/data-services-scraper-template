#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import codecs
import datetime
import logging
import sys

from collections import OrderedDict

import scraperwiki
from dshelpers import (update_status, download_url, install_cache,
                       batch_processor)

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
    with batch_processor(save_rows, batch_size=5000) as b:
        for row in process(fobj):
            logging.info(','.join(['{}'.format(v) for v in row.values()]))
            b.push(row)

    update_status()


def save_rows(rows):
    scraperwiki.sqlite.save(
        unique_keys=UNIQUE_KEYS,
        data=rows)


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
