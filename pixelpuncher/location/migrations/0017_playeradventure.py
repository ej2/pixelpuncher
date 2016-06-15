# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-13 04:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0023_auto_20160612_1804'),
        ('location', '0016_auto_20160613_0404'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerAdventure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('date_created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('date_updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
                ('adventure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='location.Adventure')),
                ('choice_made', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='location.AdventureChoice')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='player.Player')),
            ],
        ),
    ]