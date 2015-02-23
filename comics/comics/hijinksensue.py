from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'HijiNKS Ensue'
    language = 'en'
    url = 'http://hijinksensue.com/'
    start_date = '2007-05-11'
    rights = 'Joel Watson'


class Crawler(CrawlerBase):
    history_capable_days = 40
    time_zone = 'US/Central'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://hijinksensue.com/feed/')
        for entry in feed.for_date(pub_date):
            if '/comic/' not in entry.link:
                continue
            url = entry.content0.src('img.wp-post-image')
            if not url:
                continue
            url = url.replace('-300x120', '')
            title = entry.title
            return CrawlerImage(url, title)
