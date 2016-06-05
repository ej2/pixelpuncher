from __future__ import division

from django.db import models

from pixelpuncher.player.models import GENDER, AvatarLayer


class NPCAvatar(models.Model):
    name = models.CharField(max_length=25)
    body_layer = models.ForeignKey(AvatarLayer, null=True, blank=True, related_name="+")
    hair_layer = models.ForeignKey(AvatarLayer, null=True, blank=True, related_name="+")
    face_layer = models.ForeignKey(AvatarLayer, null=True, blank=True, related_name="+")
    shirt_layer = models.ForeignKey(AvatarLayer, null=True, blank=True, related_name="+")

    def __unicode__(self):
        return self.name


class NPC(models.Model):
    name = models.CharField(max_length=25)
    gender = models.CharField(max_length=1, default="M", choices=GENDER)
    level = models.IntegerField(default=1)

    total_health = models.IntegerField(default=10)
    current_health = models.IntegerField(default=10)

    total_energy = models.IntegerField(default=10)
    current_energy = models.IntegerField(default=10)

    power = models.IntegerField(default=1)
    technique = models.IntegerField(default=1)
    endurance = models.IntegerField(default=1)

    pixels = models.IntegerField(default=0)
    avatar = models.ForeignKey(NPCAvatar, null=True, blank=True)

    def __unicode__(self):
        return self.name