# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-26 19:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='current_energy',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='player',
            name='endurance',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='player',
            name='power',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='player',
            name='technique',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='player',
            name='total_energy',
            field=models.IntegerField(default=1),
        ),
    ]
