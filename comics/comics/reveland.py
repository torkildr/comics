from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Reveland'
    language = 'no'
    url = 'http://reveland.nettserier.no/'
    start_date = '2007-03-20'
    end_date = '2013-04-17'
    active = False
    rights = 'Jorunn Hanto-Haugse'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
