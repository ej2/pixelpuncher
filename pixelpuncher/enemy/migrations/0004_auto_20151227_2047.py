# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-27 20:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enemy', '0003_auto_20151226_2206'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enemy',
            options={'verbose_name': 'enemy', 'verbose_name_plural': 'enemies'},
        ),
    ]
