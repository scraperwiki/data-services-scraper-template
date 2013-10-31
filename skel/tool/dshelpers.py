#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import logging
import requests
import requests_cache

from cStringIO import StringIO

import scraperwiki

__all__ = ["update_status", "install_cache", "download_url"]


def update_status(table_name="swdata", date_column="date"):
    """
    Set the status endpoint on ScraperWiki to the latest entry e.g.
    'Latest entry: 2013-10-01'
    """
    status_text = 'Latest entry: {}'.format(
        _get_most_recent_record(table_name, date_column))
    logging.info(status_text)

    scraperwiki.status('ok', status_text)


def _get_most_recent_record(table_name, column):
    result = scraperwiki.sql.select(
        "MAX({1}) AS most_recent FROM {0} LIMIT 1".format(table_name, column))
    return result[0]['most_recent']


def install_cache(expire_after=12*3600):
    """
    Patches the requests library with requests_cache.
    """
    requests_cache.install_cache(
        expire_after=expire_after,
        allowable_methods=('GET',))


def download_url(url):
    """
    Get the content of a URL and return a file-like object.
    """
    logging.info("Download {}".format(url))
    response = requests.get(url)
    response.raise_for_status()
    return StringIO(response.content)
