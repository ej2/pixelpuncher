# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-05 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('npc', '0002_auto_20160605_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='npcavatar',
            name='name',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
    ]
