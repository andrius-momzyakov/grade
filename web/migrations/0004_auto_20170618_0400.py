# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-18 04:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_contact_contactemail_contactphone'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactemail',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Наименование адреса'),
        ),
        migrations.AddField(
            model_name='contactphone',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Наименование телефона'),
        ),
    ]
