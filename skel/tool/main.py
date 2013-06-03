#!/usr/bin/env python

import requests
import requests_cache
import scraperwiki
import lxml.html

BASE_URL = 'http://www.google.com'


def main():
    install_cache()

    html = download_url(BASE_URL)
    lxml_root = lxml.html.fromstring(html)
    process(lxml_root)
    scraperwiki.status('ok', 'Run was successful.')


def install_cache():
    requests_cache.install_cache(
        cache_name='requests_cache.sqlite',
        expire_after=(12 * 60 * 60))


def download_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.content


def process(lxml_root):
    pass

if __name__ == '__main__':
    main()
