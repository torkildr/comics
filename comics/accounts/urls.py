from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

from invitation import views as invitation_views
from registration import views as reg_views

from comics.accounts.forms import (
    AuthenticationForm, PasswordResetForm, RegistrationForm)
from comics.accounts import views as account_views

urlpatterns = patterns(
    '',

    ### django-invitation

    url(r'^invite/complete/$',
        TemplateView.as_view(
            template_name='invitation/invitation_complete.html'),
        {
            'extra_context': {'active': {
                'invite': True,
            }},
        },
        name='invitation_complete'),
    url(r'^invite/$',
        invitation_views.invite,
        {
            'extra_context': {'active': {
                'invite': True,
            }},
        },
        name='invitation_invite'),
    url(r'^invited/(?P<invitation_key>\w+)/$',
        invitation_views.invited,
        {
            'extra_context': {'active': {'register': True}},
        },
        name='invitation_invited'),
    url(r'^register/$',
        invitation_views.register,
        {
            'backend': 'comics.accounts.backends.RegistrationBackend',
            'form_class': RegistrationForm,
            'extra_context': {'active': {'register': True}},
        },
        name='registration_register'),

    ### django-registration

    #url(r'^register/$',
    #    reg_views.register,
    #    {
    #        'backend': 'comics.accounts.backends.RegistrationBackend',
    #        'extra_context': {'active': {'register': True}},
    #    },
    #    name='registration_register'),
    url(r'^register/complete/$',
        TemplateView.as_view(
            template_name='registration/registration_complete.html'),
        name='registration_complete'),
    url(r'^register/closed/$',
        TemplateView.as_view(
            template_name='registration/registration_closed.html'),
        name='registration_disallowed'),

    url(r'^activate/complete/$',
        TemplateView.as_view(
            template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$',
        reg_views.activate,
        {'backend': 'comics.accounts.backends.RegistrationBackend'},
        name='registration_activate'),

    ### django.contrib.auth

    url(r'^login/$',
        auth_views.login,
        {
            'authentication_form': AuthenticationForm,
            'extra_context': {'active': {'login': True}},
            'template_name': 'auth/login.html',
        },
        name='login'),
    url(r'^logout/$',
        auth_views.logout,
        {'next_page': '/account/login/'},
        name='logout'),

    url(r'^password/change/$',
        auth_views.password_change,
        {
            'template_name': 'auth/password_change.html',
            'extra_context': {'active': {
                'account': True,
                'password_change': True,
            }},
        },
        name='password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        {'template_name': 'auth/password_change_done.html'},
        name='password_change_done'),

    url(r'^password/reset/$',
        auth_views.password_reset,
        {
            'template_name': 'auth/password_reset.html',
            'email_template_name': 'auth/password_reset_email.txt',
            'subject_template_name': 'auth/password_reset_email_subject.txt',
            'password_reset_form': PasswordResetForm,
        },
        name='password_reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'auth/password_reset_confirm.html'},
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'auth/password_reset_complete.html'},
        name='password_reset_complete'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {'template_name': 'auth/password_reset_done.html'},
        name='password_reset_done'),

    ### comics.accounts

    url(r'^$',
        account_views.account_details, name='account'),

    url(r'^secret-key/$',
        account_views.secret_key, name='secret_key'),

    url(r'^toggle-comic/$',
        account_views.mycomics_toggle_comic, name='toggle_comic'),

    url(r'^edit-comics/$',
        account_views.mycomics_edit_comics, name='edit_comics'),
)

if 'comics.sets' in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        '',
        url(r'^import-set/$',
            account_views.mycomics_import_named_set, name='import_named_set'),
    )
