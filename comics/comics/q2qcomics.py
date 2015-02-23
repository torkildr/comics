from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Q2Q Comics'
    language = 'en'
    url = 'http://q2qcomics.com/'
    start_date = '2014-03-08'
    rights = 'Steve Younkins'


class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,We,Fr'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://q2qcomics.com/feed/')
        for entry in feed.for_date(pub_date):
            if 'Comics' not in entry.tags:
                continue
            url = entry.content0.src('img.size-full')
            title = entry.title.replace('Q2Q Comics ', '')
            return CrawlerImage(url, title)
