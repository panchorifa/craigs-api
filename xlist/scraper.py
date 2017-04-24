import requests
from lxml import html
from models import Item, City, State, Category


_REGION_PATH = '//div[@class="jump_to_continents"]/a/@href'
_STATE_PATH = '//parent::ul'
_ITEM_PATH = '//li[@class="result-row"]'
_CATEGORY_PATH = '//div[@class="col"]'
_CATEGORY_NAME_PATH = 'h4/a'
_CATEGORY_URL_PATH = 'h4/a/@href'
_DATE_PATH = 'p[@class="result-info"]/time[@datetime]'
_TITLE_PATH = 'p[@class="result-info"]/a/[@class="result-title hdrlnk"]'
_URL_PATH = 'p[@class="result-info"]/a[@class="result-title hdrlnk"]/@href'
_IMAGE_PATH = 'a[@class="result-image gallery"]/@data-ids'


class HtmlScraper(object):
    def __init__(self, text):
        """
        Html scraper
        :parse text: html text
        """
        self.tree = html.fromstring(text)
        self.item_paths = self.tree.xpath(_ITEM_PATH)
        print('found: {} paths'.format(len(self.item_paths)))
        print('found: {}'.format(self.item_paths[0].findtext(_DATE_PATH)))
        print('found: {}'.format(self.item_paths[0].findtext(_TITLE_PATH)))
        print('found: {}'.format(self.item_paths[0].xpath(_URL_PATH)[0]))
        print('found: {}'.format(self.item_paths[0].xpath(_IMAGE_PATH)))

    def scrape_item(self, path, keywords):
        """
        Returns an Item instance when keywords are found
        :param path: item xpath
        :param keywords: search keywords
        """
        _date = path.findtext(_DATE_PATH)
        _title = path.findtext(_TITLE_PATH).encode('ascii', 'ignore')
        _url = path.xpath(_URL_PATH)[0]
        _image = path.xpath(_IMAGE_PATH)
        _image = _image[0].split(',')[0] if _image else None
        return Item(_date, _title, _url, _image, keywords=keywords)


def _us(text):
    us = '<div>'
    active = False
    for line in text.split('\n'):
        line = line.strip()
        if line == '<h1><a name="US"></a>US</h1>':
            active = True
        elif active and line.startswith('<h4>'):
            us += '\n</div>\n<div>\n' + line + '\n'
        elif active and line.startswith('<h1>'):
            break
        elif active:
            us += line+'\n'
    return '{}\n</div>\n'.format(us)


class CitiesScraper(object):
    def __init__(self, text):
        """
        Scraper to find craigslist cities
        :param text: html
        """
        self.tree = html.fromstring(_us(text))
        self.item_paths = self.tree.xpath(_STATE_PATH)
        print('found: {}'.format(len(self.item_paths)))

    def scrape_state(self, path):
        """
        Scrapes a state path
        :returns: List of cities for the given state path.
        """
        cities = []

        for li in path.xpath('li'):
            # print '>>>', li.findtext('a'), li.xpath('a/@href')[0]
            cities.append(City(li.findtext('a'), li.xpath('a/@href')[0]))
        return State(path.findtext('..h4'), cities)


class RegionsScraper(object):
    def __init__(self, text):
        """
        Scraper to find craigslist regions
        :param text: html
        """
        self.tree = html.fromstring(text)
        self.regions = self.tree.xpath(_REGION_PATH)
        print('found: {}'.format(len(self.regions)))
        self.regions = [self.region(x[1:]) for x in self.regions]

    def region(self, x):
        return {
            'name': x,
            'link': '/{}/cities'.format(x)
        }


class CategoriesScraper(object):
    def __init__(self, text):
        """
        Scrapes a craigslist city to find categories
        :param text: html
        """
        self.tree = html.fromstring(text)
        self.item_paths = self.tree.xpath(_CATEGORY_PATH)

    def scrape_category(self, path):
        _name = path.findtext(_CATEGORY_NAME_PATH)
        _url = path.xpath(_CATEGORY_URL_PATH)
        if _url:
            items = []
            print "    'name':'{}', 'url':'{}', 'cats':".format(_name, _url[0])
            for li in path.xpath('div/ul/li'):
                _li_name = li.findtext('a').encode('ascii', 'ignore').strip()
                _li_url = li.xpath('a/@href')[0].encode('ascii', 'ignore').strip()
                print "        'name':'{}', 'url':'{}',".format(_li_name, _li_url)
                items.append(Category(_li_name, _li_url))
            return Category(_name, _url, items)
        return None
