# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 01:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0007_auto_20151230_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='attribute_points',
            field=models.IntegerField(default=0),
        ),
    ]
