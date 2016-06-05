# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-05 03:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NPC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('gender', models.CharField(choices=[(b'M', b'Male'), (b'F', b'Female')], default=b'M', max_length=1)),
                ('level', models.IntegerField(default=1)),
                ('total_health', models.IntegerField(default=1)),
                ('current_health', models.IntegerField(default=1)),
                ('total_energy', models.IntegerField(default=1)),
                ('current_energy', models.IntegerField(default=1)),
                ('power', models.IntegerField(default=1)),
                ('technique', models.IntegerField(default=1)),
                ('endurance', models.IntegerField(default=1)),
                ('pixels', models.IntegerField(default=0)),
            ],
        ),
    ]
