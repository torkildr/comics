# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations

import comics.accounts.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('comic', models.ForeignKey(to='core.Comic')),
            ],
            options={
                'db_table': 'comics_user_profile_comics',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False,
                    auto_created=True, primary_key=True)),
                ('secret_key',
                    models.CharField(
                        default=comics.accounts.models.make_secret_key,
                        help_text=b'Secret key for feed and API access',
                        max_length=32)),
                ('comics', models.ManyToManyField(to='core.Comic',
                    through='accounts.Subscription')),
                ('user', models.OneToOneField(related_name=b'comics_profile',
                    to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comics_user_profile',
                'verbose_name': 'comics profile',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='subscription',
            name='userprofile',
            field=models.ForeignKey(to='accounts.UserProfile'),
            preserve_default=True,
        ),
    ]
