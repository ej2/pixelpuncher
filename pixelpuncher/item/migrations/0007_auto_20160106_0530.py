# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-06 05:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_itemtype_level_requirement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtype',
            name='classification',
            field=models.CharField(choices=[(b'GLOVE', b'Gloves'), (b'HEAD', b'Head'), (b'TORSO', b'Torso'), (b'FOOD', b'Food'), (b'DRINK', b'Drink')], max_length=6),
        ),
    ]
