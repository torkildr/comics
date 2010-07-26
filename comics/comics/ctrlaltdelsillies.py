from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Ctrl+Alt+Del Sillies'
    language = 'en'
    url = 'http://www.cad-comic.com/sillies/'
    start_date = '2008-06-27'
    rights = 'Tim Buckley'

class Crawler(CrawlerBase):
    history_capable_date = '2008-06-27'
    time_zone = -5

    # Without User-Agent set, the server returns empty responses
    headers = {'User-Agent': 'Mozilla/4.0'}

    def crawl(self, pub_date):
        page = self.parse_page('http://www.cad-comic.com/sillies/%s' %
            pub_date.strftime('%Y%m%d'))
        url = page.src('img[src*="/comics/"]')
        return CrawlerImage(url)
