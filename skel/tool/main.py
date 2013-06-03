#!/usr/bin/env python

import requests
import requests_cache
import scraperwiki

BASE_URL = 'http://www.google.com'


def main():
    install_cache()

    html = download_url(BASE_URL)
    process(html)
    scraperwiki.status('ok', 'Run was successful.')


def install_cache():
    requests_cache.install_cache(
        cache_name='requests_cache.sqlite',
        expire_after=(12 * 60 * 60))


def download_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def process(html):
    pass

if __name__ == '__main__':
    main()
