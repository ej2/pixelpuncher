# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-04 01:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_auto_20160103_0556'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtype',
            name='armor_rating',
            field=models.IntegerField(default=0),
        ),
    ]
