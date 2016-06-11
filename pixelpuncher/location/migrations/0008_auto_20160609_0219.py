# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-09 02:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0007_auto_20160609_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_type',
            field=models.CharField(choices=[(b'HEAL', b'Healing'), (b'REST', b'Rest'), (b'HEALMAX', b'Restore Health'), (b'RESTMAX', b'Restore Energy')], max_length=7),
        ),
    ]