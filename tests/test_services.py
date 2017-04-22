"""
services tests
"""
from xlist.services import XlistService
from xlist.settings import CITIES_URL
from core import XRequests


BOSTON_SAMPLE_HTML = 'tests/samples/boston.html'
US_SAMPLE_HTML = 'tests/samples/us.html'


URLS = {
    'http://boston.craigslist.org/sof': BOSTON_SAMPLE_HTML,
    'http://www.craigslist.org/about/sites#US': US_SAMPLE_HTML
}


xrequests = XRequests(URLS)
service = XlistService(xrequests)


def test_find_all():
    categories, cities, keywords = ['sof'], ['boston'], ['']
    results = service.find(categories, keywords, cities)
    assert(len(results) == 1)
    assert(results[0].city == 'boston')
    assert(results[0].cat == 'sof')
    print len(results[0].items)
    assert(len(results[0].items) == 4)

def test_find_java():
    categories, cities, keywords = ['sof'], ['boston'], ['java']
    results = service.find(categories, keywords, cities)
    assert(len(results) == 1)
    assert(len(results[0].items) == 1)   
    item = results[0].items[0]
    assert(item.title=='JAVA Developer  (Boston near North and South Station)')
    assert(item.url=='http://boston.craigslist.org/gbs/sof/4286078333.html')

def test_cities():
    _region = service.cities('US')
    assert(len(_region.states) == 52)    
    alabama = _region.states[0]
    assert(alabama.name == 'Alabama')
    assert(len(alabama.cities) == 9)
    tuscaloosa = alabama.cities[8]
    assert(tuscaloosa.name == 'tuscaloosa')
    assert(tuscaloosa.url == 'http://tuscaloosa.craigslist.org')
    territories = _region.states[51]
    assert(territories.name == 'Territories')
    assert(len(territories.cities) == 3)
