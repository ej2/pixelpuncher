# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-04 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('player', '0020_auto_20160604_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('active', models.BooleanField(default=True)),
                ('location_type', models.CharField(choices=[(b'ADV', b'Adventure'), (b'MED', b'Medical'), (b'SHP', b'Shop'), (b'TRN', b'Training')], max_length=3)),
                ('icon', models.CharField(blank=True, max_length=50, null=True)),
                ('players', models.ManyToManyField(blank=True, related_name='locations', to='player.Player')),
            ],
        ),
    ]
