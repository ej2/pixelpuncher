# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-21 02:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enemy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enemy',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
