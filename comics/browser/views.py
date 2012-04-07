from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView, ListView, DayArchiveView, MonthArchiveView, RedirectView)

from comics.core.models import Comic, Release


class LoginRequiredMixin(object):
    """Things common for views requiring the user to be logged in"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        # This overide is here so that the login_required decorator can be
        # applied to all the views subclassing this class.
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class ComicMixin(LoginRequiredMixin):
    """Things common for *all* views of comics"""

    @property
    def comic(self):
        if not hasattr(self, '_comic'):
            self._comic = None
        if not self._comic and 'comic_slug' in self.kwargs:
            self._comic = get_object_or_404(
                Comic, slug=self.kwargs['comic_slug'])
        return self._comic


class ReleaseMixin(ComicMixin):
    """Things common for *all* views of comic releases"""

    template_name = 'browser/release_list.html'

    def render_to_response(self, context, **kwargs):
        # We hook into render_to_response() instead of get_context_data()
        # because the date based views only populate the context with
        # date-related information right before render_to_response() is called.
        context.update(self.get_release_context_data(context))
        return super(ReleaseMixin, self).render_to_response(context, **kwargs)

    def get_release_context_data(self, context):
        # The methods called later in this method assumes that ``self.context``
        # contains what is already ready to be made available for the template.
        self.context = context

        return {
            'my_comics': self.get_my_comics(),

            'active': {'home': True},
            'view_type': self.get_view_type(),

            'title': self.get_title(),
            'subtitle': self.get_subtitle(),

            'latest_url': self.get_latest_url(),
            'day_url': self.get_day_url(),
            'month_url': self.get_month_url(),
            'feed_url': self.get_feed_url(),
            'feed_title': self.get_feed_title(),

            'first_url': self.get_first_url(),
            'prev_url': self.get_prev_url(),
            'next_url': self.get_next_url(),
            'last_url': self.get_last_url(),
        }

    def get_my_comics(self):
        return self.request.user_set.comics.all()

    def get_view_type(self):
        return None

    def get_title(self):
        return None

    def get_subtitle(self):
        return None

    def get_latest_url(self):
        return None

    def get_day_url(self):
        return None

    def get_month_url(self):
        return None

    def get_feed_url(self):
        return None

    def get_feed_title(self):
        return None

    def get_first_url(self):
        return None

    def get_prev_url(self):
        return None

    def get_next_url(self):
        return None

    def get_last_url(self):
        return None


class ReleaseLatestView(ReleaseMixin, ListView):
    """Things common for all *latest* views"""

    def get_subtitle(self):
        return 'Latest'

    def get_view_type(self):
        return 'latest'


class ReleaseDateMixin(ReleaseMixin):
    """Things common for all *date based* views"""

    date_field = 'pub_date'
    month_format = '%m'


class ReleaseDayArchiveView(ReleaseDateMixin, DayArchiveView):
    """Things common for all *day* views"""

    def get_view_type(self):
        return 'day'

    def get_subtitle(self):
        return self.context['day'].strftime('%A %d %B %Y').replace(' 0', ' ')


class ReleaseMonthArchiveView(ReleaseDateMixin, MonthArchiveView):
    """Things common for all *month* views"""

    def get_view_type(self):
        return 'month'

    def get_subtitle(self):
        return self.context['month'].strftime('%B %Y')


class MyComicsMixin(object):
    """Things common for all views of *my comics*"""

    def get_queryset(self):
        return Release.objects.filter(comic__in=self.get_my_comics())

    def get_title(self):
        return 'My comics'

    def get_latest_url(self):
        return reverse('mycomics_latest')

    def get_day_url(self):
        last_date = self.get_queryset().dates('pub_date', 'day', 'DESC')[0]
        if last_date:
            return reverse('mycomics_day', kwargs={
                'year': last_date.year,
                'month': last_date.month,
                'day': last_date.day,
            })

    def get_month_url(self):
        last_month = self.get_queryset().dates('pub_date', 'month', 'DESC')[0]
        if last_month:
            return reverse('mycomics_month', kwargs={
                'year': last_month.year,
                'month': last_month.month,
            })

    def get_feed_url(self):
        return '%s?key=%s' % (reverse('mycomics_feed'),
            self.request.user.get_profile().secret_key)

    def get_feed_title(self):
        return 'Feed for %s' % self.request.user.email


class MyComicsHome(LoginRequiredMixin, RedirectView):
    """Redirects the home page to my comics"""

    def get_redirect_url(self, **kwargs):
        return reverse('mycomics_latest')


class MyComicsLatestView(MyComicsMixin, ReleaseLatestView):
    """View of the latest releases from my comics"""

    paginate_by = 100

    def get_queryset(self):
        releases = super(MyComicsLatestView, self).get_queryset()
        return releases.order_by('-fetched')

    def get_first_url(self):
        page = self.context['page_obj']
        if page.number != page.paginator.num_pages:
            return reverse('mycomics_latest_page_n',
                kwargs={'page': page.paginator.num_pages})

    def get_prev_url(self):
        page = self.context['page_obj']
        if page.has_next():
            return reverse('mycomics_latest_page_n',
                kwargs={'page': page.next_page_number()})

    def get_next_url(self):
        page = self.context['page_obj']
        if page.has_previous():
            return reverse('mycomics_latest_page_n',
                kwargs={'page': page.previous_page_number()})

    def get_last_url(self):
        page = self.context['page_obj']
        if page.number != 1:
            return reverse('mycomics_latest_page_n', kwargs={'page': 1})


class MyComicsDayView(MyComicsMixin, ReleaseDayArchiveView):
    """View of releases from my comics for a given day"""

    def get_first_url(self):
        first_date = self.get_queryset().dates(self.date_field, 'day')[0]
        if first_date and first_date.date() < self.context['day']:
            return reverse('mycomics_day', kwargs={
                'year': first_date.year,
                'month': first_date.month,
                'day': first_date.day,
            })

    def get_prev_url(self):
        prev_date = self.get_previous_day(self.context['day'])
        if prev_date:
            return reverse('mycomics_day', kwargs={
                'year': prev_date.year,
                'month': prev_date.month,
                'day': prev_date.day,
            })

    def get_next_url(self):
        next_date = self.get_next_day(self.context['day'])
        if next_date:
            return reverse('mycomics_day', kwargs={
                'year': next_date.year,
                'month': next_date.month,
                'day': next_date.day,
            })

    def get_last_url(self):
        last_date = self.get_queryset().dates(
            self.date_field, 'day', 'DESC')[0]
        if last_date and last_date.date() > self.context['day']:
            return reverse('mycomics_day', kwargs={
                'year': last_date.year,
                'month': last_date.month,
                'day': last_date.day,
            })


class MyComicsMonthView(MyComicsMixin, ReleaseMonthArchiveView):
    """View of releases from my comics for a given month"""

    def get_first_url(self):
        first_month = self.get_queryset().dates(self.date_field, 'month')[0]
        if first_month and first_month.date() < self.context['month']:
            return reverse('mycomics_month', kwargs={
                'year': first_month.year,
                'month': first_month.month,
            })

    def get_prev_url(self):
        prev_month = self.context['previous_month']
        if prev_month:
            return reverse('mycomics_month', kwargs={
                'year': prev_month.year,
                'month': prev_month.month,
            })

    def get_next_url(self):
        next_month = self.context['next_month']
        if next_month:
            return reverse('mycomics_month', kwargs={
                'year': next_month.year,
                'month': next_month.month,
            })

    def get_last_url(self):
        last_month = self.get_queryset().dates(
            self.date_field, 'month', 'DESC')[0]
        if last_month and last_month.date() > self.context['month']:
            return reverse('mycomics_month', kwargs={
                'year': last_month.year,
                'month': last_month.month,
            })


class MyComicsYearView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        return reverse('mycomics_month', kwargs={
            'year': kwargs['year'],
            'month': '1',
        })


class OneComicMixin(object):
    """Things common for all views of a single comic"""

    def get_queryset(self):
        return Release.objects.filter(comic=self.comic)

    def get_title(self):
        return self.comic.name

    def get_latest_url(self):
        return reverse('comic_latest', kwargs={'comic_slug': self.comic.slug})

    def get_day_url(self):
        last_date = self.get_queryset().dates('pub_date', 'day', 'DESC')[0]
        if last_date:
            return reverse('comic_day', kwargs={
                'comic_slug': self.comic.slug,
                'year': last_date.year,
                'month': last_date.month,
                'day': last_date.day,
            })

    def get_month_url(self):
        last_month = self.get_queryset().dates('pub_date', 'month', 'DESC')[0]
        if last_month:
            return reverse('comic_month', kwargs={
                'comic_slug': self.comic.slug,
                'year': last_month.year,
                'month': last_month.month,
            })

    def get_feed_url(self):
        return '%s?key=%s' % (
            reverse('comic_feed', kwargs={'comic_slug': self.comic.slug}),
            self.request.user.get_profile().secret_key)

    def get_feed_title(self):
        return 'Feed for %s' % self.comic.name


class OneComicLatestView(OneComicMixin, ReleaseLatestView):
    """View of the latest release from a single comic"""

    paginate_by = 1

    def get_queryset(self):
        release = super(OneComicLatestView, self).get_queryset()
        return release.order_by('-fetched')


class OneComicDayView(OneComicMixin, ReleaseDayArchiveView):
    """View of the releases from a single comic for a given day"""

    def get_first_url(self):
        first_date = self.get_queryset().dates(self.date_field, 'day')[0]
        if first_date and first_date.date() < self.context['day']:
            return reverse('comic_day', kwargs={
                'comic_slug': self.comic.slug,
                'year': first_date.year,
                'month': first_date.month,
                'day': first_date.day,
            })

    def get_prev_url(self):
        prev_date = self.get_previous_day(self.context['day'])
        if prev_date:
            return reverse('comic_day', kwargs={
                'comic_slug': self.comic.slug,
                'year': prev_date.year,
                'month': prev_date.month,
                'day': prev_date.day,
            })

    def get_next_url(self):
        next_date = self.get_next_day(self.context['day'])
        if next_date:
            return reverse('comic_day', kwargs={
                'comic_slug': self.comic.slug,
                'year': next_date.year,
                'month': next_date.month,
                'day': next_date.day,
            })

    def get_last_url(self):
        last_date = self.get_queryset().dates(
            self.date_field, 'day', 'DESC')[0]
        if last_date and last_date.date() > self.context['day']:
            return reverse('comic_day', kwargs={
                'comic_slug': self.comic.slug,
                'year': last_date.year,
                'month': last_date.month,
                'day': last_date.day,
            })


class OneComicMonthView(OneComicMixin, ReleaseMonthArchiveView):
    """View of the releases from a single comic for a given month"""

    def get_first_url(self):
        first_month = self.get_queryset().dates(self.date_field, 'month')[0]
        if first_month and first_month.date() < self.context['month']:
            return reverse('comic_month', kwargs={
                'comic_slug': self.comic.slug,
                'year': first_month.year,
                'month': first_month.month,
            })

    def get_prev_url(self):
        prev_month = self.context['previous_month']
        if prev_month:
            return reverse('comic_month', kwargs={
                'comic_slug': self.comic.slug,
                'year': prev_month.year,
                'month': prev_month.month,
            })

    def get_next_url(self):
        next_month = self.context['next_month']
        if next_month:
            return reverse('comic_month', kwargs={
                'comic_slug': self.comic.slug,
                'year': next_month.year,
                'month': next_month.month,
            })

    def get_last_url(self):
        last_month = self.get_queryset().dates(
            self.date_field, 'month', 'DESC')[0]
        if last_month and last_month.date() > self.context['month']:
            return reverse('comic_month', kwargs={
                'comic_slug': self.comic.slug,
                'year': last_month.year,
                'month': last_month.month,
            })


class OneComicYearView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, **kwargs):
        return reverse('comic_month', kwargs={
            'comic_slug': kwargs['comic_slug'],
            'year': kwargs['year'],
            'month': '1',
        })


class OneComicWebsiteRedirect(ComicMixin, TemplateView):
    template_name = 'browser/comic_website.html'

    def get_context_data(self, **kwargs):
        context = super(OneComicWebsiteRedirect, self).get_context_data(
            **kwargs)
        context['url'] = self.comic.url
        return context