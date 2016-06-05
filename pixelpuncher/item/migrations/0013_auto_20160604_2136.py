# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-04 21:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0012_itemtype_combat_usable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtype',
            name='classification',
            field=models.CharField(choices=[(b'GLOVE', b'Gloves'), (b'HEAD', b'Head'), (b'TORSO', b'Torso'), (b'FOOD', b'Food'), (b'DRINK', b'Drink'), (b'MISC', b'Misc')], max_length=6),
        ),
    ]
