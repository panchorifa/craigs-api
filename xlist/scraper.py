import requests
from lxml import html
from settings import CITY_URL
from models import Item, City, State, Category


_STATE_PATH = '//parent::ul'
_ITEM_PATH = '//p[@class="row"]'
_CATEGORY_PATH = '//div[@class="col"]'
_CATEGORY_NAME_PATH = 'h4/a'
_CATEGORY_URL_PATH = 'h4/a/@href'
_DATE_PATH = 'span[@class="txt"]/span[@class="pl"]/time'
_TITLE_PATH = 'span[@class="txt"]/span[@class="pl"]/a'
_URL_PATH = 'span[@class="txt"]/span[@class="pl"]/a/@href'
_DETAILS_PATH = 'span[@class="txt"]/span[@class="l2"]/span[@class="pnr"]/small'


class HtmlScraper(object):
    def __init__(self, text):
        """
        Html scraper
        :parse text: html text
        """
        self.tree = html.fromstring(text)
        self.item_paths = self.tree.xpath(_ITEM_PATH)
        print('found: {} paths'.format(len(self.item_paths)))

    def scrape_item(self, path, keywords):
        """
        Returns an Item instance when keywords are found
        :param path: item xpath
        :param keywords: search keywords
        """
        _date = path.findtext(_DATE_PATH)
        _title = path.findtext(_TITLE_PATH).encode('ascii', 'ignore')
        _url = path.xpath(_URL_PATH)[0]
        _details = path.findtext(_DETAILS_PATH)
        _details = _details.encode('ascii', 'ignore') if _details else ''
        _title_details = '{} {}'.format(_title, _details)

        for keyword in keywords:
            if keyword.upper() in _title_details.upper():
                return Item(_date, _title_details, _url, keyword=keyword)
        return None


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