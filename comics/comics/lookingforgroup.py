from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Looking For Group'
    language = 'en'
    url = 'http://www.lfgcomic.com/'
    start_date = '2006-11-06'
    rights = 'Ryan Sohmer & Lar deSouza'


class Crawler(CrawlerBase):
    history_capable_date = '2006-11-06'
    schedule = 'Mo,Th'
    time_zone = 'America/Montreal'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/LookingForGroup')
        images = []
        for entry in feed.for_date(pub_date):
            if not entry.title.isdigit():
                continue
            url = entry.summary.src(
                'a[rel="bookmark"] img[src*="lfgcomic.com/wp-content/"]')
            if url:
                url = url.replace('-210x300', '')
            title = entry.title
            images.append(CrawlerImage(url, title))
        if images:
            return images
