"""
xlist models
"""
from settings import SEARCH_URL


class City(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
        idx = url.find('.craigslist.org')
        self.uri = url[8:idx]

class State(object):
    def __init__(self, name, cities):
        self.name = name
        self.cities = cities
        self.city_names = [c.uri for c in cities]

    def json(self):
        return [{'city':c.name, 'url':c.url} for c in self.cities]


class Region(object):
    def __init__(self, name, states):
        self.name = name
        self.states = states
        self.city_names = []
        for state in self.states:
            for city in state.city_names:
                self.city_names.append(city)

    def json(self):
        return {s.name: s.json() for s in self.states}


class CityItems(object):
    def __init__(self, city, cat, keywords):
        self.city = city
        self.cat = cat
        self.keywords = keywords
        self.url = SEARCH_URL.format(city, cat, '+'.join(keywords))
        self._items = []

    def add_item(self, item):
        item.url = self._build_item_url(item.url)
        self._items.append(item)

    @property
    def items(self):
        return self._items

    def _build_item_url(self, value):
        if value.startswith('http'):
            return value
        prefix = self.url[0:(self.url.find('.craigslist.org')+15)]
        return '{}{}'.format(prefix, value)

    def __str__(self):
        return '{} ({})'.format(self.city, self.cat)

    def json(self):
        return {'city': self.city, 'cat': self.cat, 'keywords': self.keywords,
                'url': self.url, 'items': [i.__dict__ for i in self.items]}


class Item(object):
    def __init__(self, date, title, url, image, keywords):
        self.date = date
        self.title = title
        self.url = url
        self.keywords = keywords
        self.image = 'https://images.craigslist.org/{}'.format(image) if image else ''

    def __str__(self):
        return '[{}] {}: {}'.format(self.date, self.keywords, self.title)


class Category(object):
    def __init__(self, name, url, items=[]):
        self.name = name
        self.url =url
        self.items = items
