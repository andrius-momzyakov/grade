# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-30 01:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_contactphone_place_on_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactemail',
            name='place_on_header',
            field=models.BooleanField(default=False, verbose_name='Размещать в заголовке'),
        ),
        migrations.AddField(
            model_name='contactperson',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Фото'),
        ),
    ]
