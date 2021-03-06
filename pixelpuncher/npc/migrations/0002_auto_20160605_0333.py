# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-05 03:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0020_auto_20160604_1602'),
        ('npc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NPCAvatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_layer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='player.AvatarLayer')),
                ('face_layer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='player.AvatarLayer')),
                ('hair_layer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='player.AvatarLayer')),
                ('shirt_layer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='player.AvatarLayer')),
            ],
        ),
        migrations.AddField(
            model_name='npc',
            name='avatar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='npc.NPCAvatar'),
        ),
    ]
