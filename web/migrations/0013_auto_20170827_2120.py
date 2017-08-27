# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-27 18:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20170827_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectcomment',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 27, 21, 20, 3, 837795)),
        ),
        migrations.AlterField(
            model_name='projectcomment',
            name='update_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 27, 21, 20, 3, 837829)),
        ),
        migrations.AlterField(
            model_name='projectcommentatorsecret',
            name='secret',
            field=models.CharField(default='123456', max_length=20, unique=True, verbose_name='Секретный код'),
        ),
    ]
