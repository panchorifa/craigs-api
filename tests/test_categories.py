"""
services tests
"""
from xlist.scraper import CategoriesScraper


CATEGORIES_SAMPLE_HTML = 'tests/samples/categories.html'


def test_categories():
    html_text = open(CATEGORIES_SAMPLE_HTML).read()
    scraper = CategoriesScraper(html_text)
    categories = {}
    for path in scraper.item_paths:
        cat = scraper.scrape_category(path)
        if cat:
            categories[cat.name] = cat
    assert(len(categories) == 8)
    gigs = categories['gigs']
    assert(len(gigs.items)==8)
    items = gigs.items
    assert(items[0].name=='crew' and items[0].url=='cwg/')
    assert(items[1].name=='event' and items[1].url=='evg/')
    assert(items[2].name=='labor' and items[2].url=='lbg/')
    assert(items[3].name=='talent' and items[3].url=='tlg/')
    assert(items[4].name=='computer' and items[4].url=='cpg/')
    assert(items[5].name=='creative' and items[5].url=='crg/')
    assert(items[6].name=='domestic' and items[6].url=='dmg/')
    assert(items[7].name=='writing' and items[7].url=='wrg/')
