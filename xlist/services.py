"""
Functionality to find craigslist items by city and category
"""
from scraper import HtmlScraper, RegionsScraper, CitiesScraper
from models import CityItems, Region
from settings import REGIONS_URL, CITIES_URL, CATEGORIES as _categories
import time

_cache = {}


class XlistService(object):
    def __init__(self, request_api):
        self.xrequests = request_api

    def categories(self):
        ts = time.time()
        if 'categories' not in _cache:
            _cache['categories'] = _categories
        te = time.time() - ts
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", te
        return _cache['categories']

    def regions(self):
        if 'regions' not in _cache:
            _xregions = []
            text = self.xrequests.get(REGIONS_URL)
            if text:
                scraper = RegionsScraper(text)
                _xregions = scraper.regions
            _cache['regions'] = _xregions
        return _cache['regions']

    def region(self, region):
        """
        Provide craigslist cities for the given region
        :param region: region
        :returns region: Region instance
        """
        if region in _cache:
            return _cache[region]

        states = []
        text = self.xrequests.get(CITIES_URL.format(region))
        if text:
            scraper = CitiesScraper(text)
            for path in scraper.item_paths:
                state = scraper.scrape_state(path)
                states.append(state)
        else:
            print 'ERROR: Invalid city: {}'.format(city)
        r = Region(region, states)
        _cache[region] = r
        return r

    def city_list(self, region):
        """
        Provide list of craigslist cities: {}.craigslist.org
        """
        return [ c for c in self.region(region).city_names ]

    def find_by_city(self, city, cat, keywords):
        """
        Find items by city
        :param city: city
        :param cat: category
        :param keywords: keywords
        """
        print('--------{}:{}------'.format(city, cat))
        city_items = CityItems(city, cat, keywords)
        text = self.xrequests.get(city_items.url)
        if text:
            scraper = HtmlScraper(text)
            for path in scraper.item_paths:
                item = scraper.scrape_item(path, keywords)
                if item:
                    print item
                    city_items.add_item(item)
        else:
            print 'ERROR: Invalid city: {}'.format(city)
        return city_items


    def find(self, categories, keywords, cities):
        """
        Finds craigslist data in different cities
        :param categories: List of craigslist categories (ie: sof - Software jobs)
        :param keywords: List of keywords to look for
        :para cities: List of cities to look into
        :returns: List of CityItems instances
        """
        results = []
        cities = cities if cities else self.city_list('US')
        for city in cities:
            for cat in categories:
                city_items = self.find_by_city(city, cat, keywords)
                results.append(city_items)
        return results
