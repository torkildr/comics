from django.conf.urls.defaults import patterns, url

from comics.browser import feeds, views

YEAR = r'(?P<year>(19|20)\d{2})'                   # 1900-2099
MONTH = r'(?P<month>(0*[1-9]|1[0-2]))'             # 1-12
WEEK = r'week/(?P<week>(0*[1-9]|[1-4]\d|5[0-3]))'  # 1-53
DAY = r'(?P<day>(0*[1-9]|[1-2]\d|3[0-1]))'         # 1-31
DAYS = r'\+(?P<days>\d+)'
COMIC = r'(?P<comic_slug>[0-9a-z-_]+)'

urlpatterns = patterns('',
    url(r'^$',
        views.MyComicsHome.as_view(),
        name='home'),

    # Views of my comics selection
    url(r'^my/$',
        views.MyComicsLatestView.as_view(),
        name='mycomics_latest'),
    url(r'^my/page(?P<page>[0-9]+)/$',
        views.MyComicsLatestView.as_view(),
        name='mycomics_latest_page_n'),
    url(r'^my/%s/$' % (YEAR,),
        views.MyComicsYearView.as_view(),
        name='mycomics_year'),
    url(r'^my/%s/%s/$' % (YEAR, MONTH),
        views.MyComicsMonthView.as_view(),
        name='mycomics_month'),
    url(r'^my/%s/%s/%s/$' % (YEAR, MONTH, DAY),
        views.MyComicsDayView.as_view(),
        name='mycomics_day'),
    url(r'^my/feed/$',
        feeds.MyComicsFeed(),
        name='mycomics_feed'),

    # Views of a single comic
    url(r'^%s/$' % (COMIC,),
        views.OneComicLatestView.as_view(),
        name='comic_latest'),
    url(r'^%s/%s/$' % (COMIC, YEAR),
        views.OneComicYearView.as_view(),
        name='comic_year'),
    url(r'^%s/%s/%s/$' % (COMIC, YEAR, MONTH),
        views.OneComicMonthView.as_view(),
        name='comic_month'),
    url(r'^%s/%s/%s/%s/$' % (COMIC, YEAR, MONTH, DAY),
        views.OneComicDayView.as_view(),
        name='comic_day'),
    url(r'^%s/website/$' % (COMIC,),
        views.OneComicWebsiteRedirect.as_view(),
        name='comic_website'),
    url(r'^%s/feed/$' % (COMIC,),
        feeds.OneComicFeed(),
        name='comic_feed'),
)