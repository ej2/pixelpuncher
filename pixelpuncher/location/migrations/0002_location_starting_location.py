# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-04 18:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='starting_location',
            field=models.BooleanField(default=False),
        ),
    ]
