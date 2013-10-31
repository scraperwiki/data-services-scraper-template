#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import logging
import requests
import requests_cache
import time

from nose.tools import assert_equal, assert_raises

from cStringIO import StringIO

import scraperwiki

_RECOVERABLE_CODES = [500, 503]
_MAX_RETRIES = 5

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


def install_cache(expire_after=12 * 3600):
    """
    Patches the requests library with requests_cache.
    """
    requests_cache.install_cache(
        expire_after=expire_after,
        allowable_methods=('GET',))


def download_url(url, back_off=True):
    """
    Get the content of a URL and return a file-like object.
    back_off=True provides retry
    """
    if back_off:
        return _download_with_backoff(url)
    else:
        return _download_without_backoff(url)


def _download_without_backoff(url):
    """
    Get the content of a URL and return a file-like object.
    """
    logging.info("Download {}".format(url))
    response = requests.get(url)
    response.raise_for_status()
    return StringIO(response.content)


def _download_with_backoff(url):
    next_delay = 10

    for n in range(0, _MAX_RETRIES):
        logging.info("Download {}".format(url))
        response = requests.get(url)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if response.status_code in _RECOVERABLE_CODES:
                logging.info(
                    "{}\nretrying in {} seconds".format(e, next_delay))
                time.sleep(next_delay)
                next_delay *= 2
            else:
                logging.exception(e)
                raise
        else:
            return StringIO(response.content)

    raise RuntimeError('Max retries exceeded for {0}'.format(url))


from mock import call, patch


@patch('dshelpers.requests.get')
def test_backoff_function_works_on_a_good_site(mock_requests_get):
    fake_response = requests.Response()
    fake_response.status_code = 200
    fake_response._content = "Hello"
    mock_requests_get.return_value = fake_response
    assert_equal("Hello", _download_with_backoff('http://fake_url.com').read())


@patch('time.sleep')
@patch('dshelpers.requests.get')
def test_backoff_function_works_after_one_failure(
        mock_requests_get, mock_sleep):

    def response_generator():
        bad_response = requests.Response()
        bad_response.status_code = 500

        good_response = requests.Response()
        good_response.status_code = 200
        good_response._content = "Hello"

        yield bad_response
        yield bad_response
        yield good_response

    mock_requests_get.side_effect = response_generator()

    assert_equal("Hello", _download_with_backoff('http://fake_url.com').read())
    assert_equal(
        [call(10), call(20)],
        mock_sleep.call_args_list)
    assert_equal(
        [call('http://fake_url.com'),
         call('http://fake_url.com'),
         call('http://fake_url.com')],
        mock_requests_get.call_args_list)


@patch('time.sleep')
@patch('dshelpers.requests.get')
def test_backoff_raises_on_five_failures(mock_requests_get, mock_sleep):
    fake_response = requests.Response()
    fake_response.status_code = 500

    mock_requests_get.return_value = fake_response
    #_download_with_backoff('http://fake_url.com')

    assert_raises(RuntimeError, lambda:
                  _download_with_backoff('http://fake_url.com'))
    assert_equal(
        [call(10), call(20), call(40), call(80), call(160)],
        mock_sleep.call_args_list)
