# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-11 02:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0020_auto_20160604_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=200)),
                ('icon', models.CharField(blank=True, max_length=20, null=True)),
                ('players', models.ManyToManyField(to='player.Player')),
            ],
        ),
    ]
