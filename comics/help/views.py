from django.contrib import messages
from django.contrib.sites.models import RequestSite, Site
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from comics.help.forms import FeedbackForm


def about(request):
    return render(request, 'help/about.html', {
        'active': {
            'help': True,
            'about': True,
        },
    })


def feedback(request):
    """Mail feedback to ADMINS"""

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            if Site._meta.installed:
                site_title = Site.objects.get_current().name
            else:
                site_title = RequestSite(request).name

            subject = 'Feedback from %s' % site_title
            message = form.cleaned_data['message']

            metadata = 'Client IP address: %s\n' % request.META['REMOTE_ADDR']
            metadata += 'User agent: %s\n' % request.META['HTTP_USER_AGENT']
            if request.user.is_authenticated():
                metadata += 'User: %s <%s>\n' % (
                    request.user.username, request.user.email)
            else:
                metadata += 'User: anonymous\n'
            message = '%s\n\n-- \n%s' % (message, metadata)

            mail_admins(subject, message)

            messages.info(request,
                'Thank you for taking the time to help improve the site! :-)')
            return HttpResponseRedirect(reverse('help_feedback'))
    else:
        form = FeedbackForm()

    return render(request, 'help/feedback.html', {
        'active': {
            'help': True,
            'feedback': True,
        },
        'feedback_form': form,
    })


def keyboard(request):
    return render(request, 'help/keyboard.html', {
        'active': {
            'help': True,
            'keyboard': True,
        },
    })