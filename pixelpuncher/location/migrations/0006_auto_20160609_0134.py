# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-09 01:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0005_auto_20160605_0312'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('service_type', models.CharField(choices=[(b'HEAL', b'Healing'), (b'REST', b'Rest')], max_length=4)),
                ('description', models.CharField(max_length=200)),
                ('min_amount', models.IntegerField(default=1)),
                ('max_amount', models.IntegerField(default=1)),
            ],
        ),
        migrations.AlterField(
            model_name='location',
            name='location_type',
            field=models.CharField(choices=[(b'ADV', b'Adventure'), (b'MED', b'Medical'), (b'SHP', b'Shop'), (b'TRN', b'Training'), (b'HOM', b'Home')], max_length=3),
        ),
        migrations.AddField(
            model_name='locationservice',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='location.Location'),
        ),
        migrations.AddField(
            model_name='locationservice',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='location.Service'),
        ),
    ]
