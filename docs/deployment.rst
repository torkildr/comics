**********
Deployment
**********

The following example documents *one way* to deploy *comics*. As *comics* is a
standard Django project with an additional batch job for , it may be deployed in
just about any way a Django project may be deployed. Please refer to `Django's
deployment documentation
<http://docs.djangoproject.com/en/dev/howto/deployment/>`_ for further details.

In the following examples we assume that we are deploying *comics* at
http://comics.example.com/, using Apache, mod_wsgi, and PostgreSQL. The Django
application and batch job is both running as the user ``comics-user``. The
static media files, like comic images, are served from
http://comics.example.com/media/, but may also be served from a different host.


Database
========

*comics* should theoretically work with any database supported by Django.
Though, development is mostly done on SQLite 3 and PostgreSQL 8.x. For
production use, PostgreSQL is the recommended choice.

.. note::

    If you are going to use SQLite in a deployment with Apache and so on, you
    need to ensure that the user the web server will be running as has write
    access to the *directory* the SQLite database file is located in.

Additional database indexes
---------------------------

Out of the box, *comics* will create a few extra database indexes that will
make it a lot more performant. In addition, creating the following indexes will
improve performance a bit more:

.. code-block:: sql

    CREATE INDEX comics_release_comic_id_pub_date
        ON comics_release (comic_id, pub_date);


Example Apache vhost
====================

This example requires your Apache to have the ``mod_wsgi`` module. For
efficient static media serving and caching, you should probably enable
``mod_deflate`` and ``mod_expires`` for ``/media`` and ``/static``.

.. code-block:: apache

    <VirtualHost *:80>
        ServerName comics.example.com
        ErrorLog /var/log/apache2/comics.example.com-error.log
        CustomLog /var/log/apache2/comics.example.com-access.log combined

        # Not used, but Apache will complain if the dir does not exist
        DocumentRoot /var/www/comics.example.com

        # Static media hosting
        Alias /media/ /path/to/comics/media/
        Alias /static/ /path/to/comics/static/

        # mod_wsgi setup
        WSGIDaemonProcess comics user=comics-user group=comics-user threads=50 maximum-requests=10000
        WSGIProcessGroup comics
        WSGIScriptAlias / /path/to/comics/comics/wsgi/__init__.py
        <Directory /path/to/comics/comics/wsgi>
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>

For details, please refer to the documentation of the `Apache
<http://httpd.apache.org/docs/>`_ and `mod_wsgi
<http://code.google.com/p/modwsgi/>`_ projects.


Available settings
==================

The Django docs got a `list of all available settings
<https://docs.djangoproject.com/en/1.4/ref/settings/>`_. Some of them are
repeated here if they are especially relevant for *comics*. In addition,
*comics* adds some settings of its own, which are all listed here as well.

.. automodule:: comics.settings.base
    :members:


Example ``settings/local.py``
=============================

To change settings, you should not change the settings files shipped with
*comics*, but instead override the settings in your own
``comics/comics/settings/local.py``.  Even if you do not want to override any
default settings, you must add a ``local.py`` which at least sets
``SECRET_KEY`` and most probably your database settings. A full ``local.py``
may look like this::

    # Local settings -- do NOT commit to a VCS

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = 'djdjdk5k4$(DA=!SDAD!)12312415151368edkfjgngnw3m!$!Dfafa'

    # You can override any settings here, like database settings.

    ADMINS = (
        ('Comics Webmaster', 'comics@example.com'),
    )
    MANAGERS = ADMINS

    # Database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'comics',
            'USER': 'comics',
            'PASSWORD': 'topsecret',
            'HOST': 'localhost',
            'PORT': '',
        }
    }

    # Internal IP addresses
    INTERNAL_IPS = ('127.0.0.1',)

    # Media
    MEDIA_ROOT = '/var/www/comics.example.com/media/'
    MEDIA_URL = 'http://comics.example.com/media/'
    STATIC_ROOT = '/var/www/comics.example.com/static/'
    STATIC_URL = 'http://comics.example.com/static/'

    # Caching
    CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
    CACHE_MIDDLEWARE_KEY_PREFIX = 'comics'

Of course, you should change most, if not all, of these settings for your own
installation. If your are not running a *memcached* server, remove the part on
caching from your ``local.py``.


.. _collecting-static-files:

Collecting static files
=======================

When you're not running in development mode, you'll need to collect the static
files from all apps into the ``STATIC_ROOT``. To do this, run::

    python manage.py collectstatic

You have to rerun this command every time you deploy changes to graphics, CSS
and JavaScript. For more details, see the Django documentation on `staticfiles
<https://docs.djangoproject.com/en/1.4/howto/static-files/>`_.


Example cronjob
===============

To get new comics, you should run ``comics_getreleases`` regularly. In
addition, you should run ``cleanupinvitation`` once in a while to remove
expired user invitations and ``cleanupregistration`` to delete expired users.
One way is to use ``cron`` e.g. by placing the following in
``/etc/cron.d/comics``:

.. code-block:: sh

    MAILTO=comics@example.com
    PYTHONPATH=/path/to/comics
    1 * * * * comics-user python /path/to/comics/manage.py comics_getreleases -v0
    1 3 * * * comics-user python /path/to/comics/manage.py cleanupinvitation -v0
    2 3 * * * comics-user python /path/to/comics/manage.py cleanupregistration -v0

If you have installed *comics*' dependencies in a virtualenv instead of
globally, the cronjob must also activate the virtualenv. This can be done by
using the ``python`` interpreter from the virtualenv:

.. code-block:: sh

    MAILTO=comics@example.com
    PYTHONPATH=/path/to/comics
    1 * * * * comics-user /path/to/comics-virtualenv/bin/python /path/to/comics/manage.py comics_getreleases -v0
    1 3 * * * comics-user /path/to/comics-virtualenv/bin/python /path/to/comics/manage.py cleanupinvitation -v0
    2 3 * * * comics-user /path/to/comics-virtualenv/bin/python /path/to/comics/manage.py cleanupregistration -v0

By setting ``MAILTO`` any exceptions raised by the comic crawlers will be sent
by mail to the given mail address. ``1 * * * *`` specifies that the command
should be run 1 minute past every hour.
