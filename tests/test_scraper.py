"""
scraper tests
"""
from xlist.scraper import HtmlScraper

JOB_SAMPLE_HTML = 'tests/samples/job.html'


def test_parse_finding():
	html_text = open(JOB_SAMPLE_HTML).read()
	scraper = HtmlScraper(html_text)
	assert(len(scraper.item_paths) == 1)

	item_path = scraper.item_paths[0]
	item = scraper.scrape_item(item_path, ['node'])
	assert(item is not None)
	assert(item.title == 'API Backend Node.js Software Developer  (allows remote)')
	assert(item.date == 'Mar 6')
	assert(item.url == '/gbs/sof/4285320206.html')
