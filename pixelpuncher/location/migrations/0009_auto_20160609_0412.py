# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-09 04:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0008_auto_20160609_0219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='location_type',
            field=models.CharField(choices=[(b'ADV', b'Adventure'), (b'MED', b'Medical'), (b'SHP', b'Shop'), (b'CAS', b'Casino'), (b'TRN', b'Training'), (b'HOM', b'Home')], max_length=3),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='service_type',
            field=models.CharField(choices=[(b'HEAL', b'Healing'), (b'REST', b'Rest'), (b'HEALMAX', b'Restore Health'), (b'RESTMAX', b'Restore Energy'), (b'GMB', b'Gambling')], max_length=7),
        ),
    ]
