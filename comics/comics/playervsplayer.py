from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Player vs Player'
    language = 'en'
    url = 'http://pvponline.com/'
    start_date = '1998-05-04'
    rights = 'Scott R. Kurtz'


class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://pvponline.com/feed/')
        for entry in feed.for_date(pub_date):
            if not entry.title.startswith('Comic:'):
                continue
            page = self.parse_page(entry.link)
            url = page.src('.comic-art img[src*="/comic/"]')
            if not url:
                continue
            title = entry.title.replace('Comic: ', '')
            return CrawlerImage(url, title)
