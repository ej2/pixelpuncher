# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-18 21:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0014_auto_20160612_0414'),
        ('npc', '0004_auto_20160612_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('health_change', models.IntegerField(default=0)),
                ('energy_change', models.IntegerField(default=0)),
                ('pixels_change', models.IntegerField(default=0)),
                ('xp_change', models.IntegerField(default=0)),
                ('reward_items', models.ManyToManyField(blank=True, related_name='_response_reward_items_+', to='item.ItemType')),
            ],
        ),
        migrations.CreateModel(
            name='ResponseTrigger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trigger_text', models.CharField(max_length=30)),
                ('trigger_type', models.CharField(choices=[(b'ASK', b'Ask about'), (b'TELL', b'Tell about')], max_length=4)),
                ('npcs', models.ManyToManyField(related_name='triggers', to='npc.NPC')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='triggers', to='npc.Response')),
            ],
        ),
    ]
