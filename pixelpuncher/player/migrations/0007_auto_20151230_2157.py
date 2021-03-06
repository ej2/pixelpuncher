# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-30 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0006_auto_20151228_0324'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='critial_percentage',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='fail_percentage',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='maximum_damage',
        ),
        migrations.RemoveField(
            model_name='skill',
            name='minimum_damage',
        ),
        migrations.AddField(
            model_name='playerskill',
            name='bonus',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerskill',
            name='critical_multipler',
            field=models.DecimalField(decimal_places=2, default=2.0, max_digits=4),
        ),
        migrations.AddField(
            model_name='playerskill',
            name='critical_percentage',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerskill',
            name='dice_sides',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerskill',
            name='energy_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerskill',
            name='hit_percentage',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='playerskill',
            name='number_of_dice',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='skill',
            name='bonus',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='skill',
            name='critical_multipler',
            field=models.DecimalField(decimal_places=2, default=2.0, max_digits=4),
        ),
        migrations.AddField(
            model_name='skill',
            name='critical_percentage',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='skill',
            name='dice_sides',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='skill',
            name='gain_frequency',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='skill',
            name='gained_critical',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='skill',
            name='gained_critical_multipler',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='skill',
            name='gained_energy_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='skill',
            name='gained_hit',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='skill',
            name='hit_percentage',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='skill',
            name='number_of_dice',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='skill',
            name='skill_type',
            field=models.CharField(choices=[(b'ATTK', b'Attack'), (b'SPCL', b'Special'), (b'HEAL', b'Heal')], default='ATTK', max_length=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skill',
            name='special_type',
            field=models.CharField(blank=True, choices=[(b'energygain', b'Energy Gain'), (b'healthgain', b'Health Gain')], max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='skill',
            name='special_value_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='skill',
            name='special_value_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='skill',
            name='special_value_3',
            field=models.IntegerField(default=0),
        ),
    ]
