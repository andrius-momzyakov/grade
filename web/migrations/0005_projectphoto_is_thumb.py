# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-18 06:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20170618_0400'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectphoto',
            name='is_thumb',
            field=models.BooleanField(default=False, verbose_name='Использовать как иконку'),
        ),
    ]