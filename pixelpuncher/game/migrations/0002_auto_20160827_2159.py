# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-27 21:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0023_auto_20160612_1804'),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_type', models.CharField(choices=[(b'B', b'Bomb'), (b'1', b'One'), (b'2', b'Two'), (b'4', b'Four'), (b'8', b'Eight'), (b'S', b'Special')], max_length=1)),
                ('flipped', models.BooleanField(default=False)),
                ('position', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='MatchGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True)),
                ('state', models.CharField(choices=[(b'PLAY', b'Playing'), (b'WIN', b'Win'), (b'LOSE', b'Lose')], default=b'PLAY', max_length=3)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.Player')),
            ],
        ),
        migrations.AddField(
            model_name='matchcard',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='game.MatchGame'),
        ),
    ]
