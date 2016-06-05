# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-14 02:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enemy', '0008_enemytype_image_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='enemytype',
            name='maximum_pixels',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='enemytype',
            name='minimum_pixels',
            field=models.IntegerField(default=0),
        ),
    ]
