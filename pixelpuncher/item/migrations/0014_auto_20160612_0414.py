# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-12 04:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0022_auto_20160612_0106'),
        ('item', '0013_auto_20160604_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemtype',
            name='layer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='player.AvatarLayer'),
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='base_type',
            field=models.CharField(choices=[(b'WEA', b'Weapon'), (b'ARM', b'Armor'), (b'CON', b'Consumable'), (b'UNL', b'Unlock')], max_length=3),
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='classification',
            field=models.CharField(choices=[(b'DRINK', b'Drink'), (b'FOOD', b'Food'), (b'GLOVE', b'Gloves'), (b'HAIR', b'Hair'), (b'HEAD', b'Head'), (b'MISC', b'Misc'), (b'SHIRT', b'Shirt'), (b'TORSO', b'Torso')], max_length=6),
        ),
    ]
