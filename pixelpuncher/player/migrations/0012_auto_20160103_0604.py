# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-03 06:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0011_auto_20160103_0555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='gloves',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='item.Item'),
        ),
        migrations.AlterField(
            model_name='player',
            name='head',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='item.Item'),
        ),
        migrations.AlterField(
            model_name='player',
            name='torso',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='item.Item'),
        ),
    ]
