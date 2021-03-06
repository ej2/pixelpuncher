# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-28 01:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('player', '0005_auto_20151227_2047'),
    ]

    operations = [
        migrations.CreateModel(
            name='DropTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('max_rate', models.IntegerField(default=100)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remaining_uses', models.IntegerField(default=0)),
                ('date_created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('date_updated', django_extensions.db.fields.ModificationDateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemDrop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drop_rate', models.IntegerField()),
                ('drop_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='item.DropTable')),
            ],
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.TextField(blank=True, null=True)),
                ('base_type', models.CharField(choices=[(b'WEA', b'Weapon'), (b'ARM', b'Armor'), (b'CON', b'Consumable')], max_length=3)),
                ('classification', models.CharField(choices=[(b'GLOVE', b'Gloves'), (b'HEAD', b'Head'), (b'FOOD', b'Food'), (b'DRINK', b'Drink')], max_length=6)),
                ('total_uses', models.IntegerField(default=0)),
                ('min_damage', models.IntegerField(default=0)),
                ('max_damage', models.IntegerField(default=0)),
                ('power_bonus', models.IntegerField(default=0)),
                ('technique_bonus', models.IntegerField(default=0)),
                ('endurance_bonus', models.IntegerField(default=0)),
                ('xp_bonus', models.IntegerField(default=0)),
                ('total_health_bonus', models.IntegerField(default=0)),
                ('total_energy_bonus', models.IntegerField(default=0)),
                ('curret_health_bonus', models.IntegerField(default=0)),
                ('current_energy_bonus', models.IntegerField(default=0)),
                ('action_verb', models.CharField(blank=True, max_length=30, null=True)),
                ('stackable', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='itemdrop',
            name='item_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='item.ItemType'),
        ),
        migrations.AddField(
            model_name='item',
            name='item_type',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='item.ItemType'),
        ),
        migrations.AddField(
            model_name='item',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='player.Player'),
        ),
    ]
