import unittest
import glob
import os
import shutil
import datetime
import httpretty

from xlist.cache import Cache


SAMPLE_CITY_URL = 'http://boston.craigslist.org/sof'
CITIES_URL =  'http://www.craigslist.org/about/sites#US'
CACHE_DIRECTORY = './tests/cache'

BOSTON_HTML = 'tests/samples/boston.html'
CITIES_HTML = 'tests/samples/us.html'


cache = Cache(CACHE_DIRECTORY)


def _clean_cache():
    _clean_dir(CACHE_DIRECTORY)

def _clean_dir(directory):
    files = glob.glob('{}/*'.format(directory))
    for f in files:
        if os.path.isfile(f):
            os.unlink(f)
        else:
            shutil.rmtree(f)

def _setup_mock_response(url, file_path):
    httpretty.register_uri(httpretty.GET, 
                           url,
                           body=open(file_path, 'r').read(),
                           content_type="text/html")

@httpretty.activate
def test_get_items():
    _clean_cache()
    _setup_mock_response(SAMPLE_CITY_URL, BOSTON_HTML)
    directory = '{}/{}'.format(CACHE_DIRECTORY, datetime.date.today())
    assert(os.path.exists(directory) == False)
    text = cache.get(SAMPLE_CITY_URL)
    assert(text is not None)
    assert(os.path.exists(directory) == True)
    assert(os.path.exists('{}/sof/boston.html'.format(directory)) == True)
    _clean_cache()


@httpretty.activate
def test_get_cities():
    _clean_cache()
    _setup_mock_response(CITIES_URL, CITIES_HTML)
    cities_file = '{}/us_cities.html'.format(CACHE_DIRECTORY)
    assert(os.path.exists(cities_file) == False)
    text = cache.get(CITIES_URL)
    assert(text is not None)
    assert(os.path.exists(cities_file) == True)
    _clean_cache()
