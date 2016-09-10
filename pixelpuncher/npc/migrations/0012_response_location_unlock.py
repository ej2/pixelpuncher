# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-03 20:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0019_auto_20160902_0335'),
        ('npc', '0011_responsetrigger_response_handler'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='location_unlock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='location.Location'),
        ),
    ]