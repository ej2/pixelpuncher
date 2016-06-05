from __future__ import division
from django.db import models

from pixelpuncher.item.models import ItemType
from pixelpuncher.npc.models import NPC
from pixelpuncher.player.models import Player


LOCATION_TYPE = (
    ("ADV", "Adventure",),
    ("MED", "Medical",),
    ("SHP", "Shop",),
    ("TRN", "Training",),
)


class Location(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True, null=True)
    active = models.BooleanField(default=True)
    location_type = models.CharField(max_length=3, choices=LOCATION_TYPE)
    icon = models.CharField(max_length=50, blank=True, null=True)
    players = models.ManyToManyField(Player, related_name='locations', blank=True)
    starting_location = models.BooleanField(default=False)  # Player starts with these locations unlocked
    npc = models.ForeignKey(NPC, null=True, blank=True)

    def __unicode__(self):
        return self.name


class LocationItem(models.Model):
    location = models.ForeignKey(Location, related_name="items")
    item_type = models.ForeignKey(ItemType)
    price = models.IntegerField()

    def __unicode__(self):
        return "{} ${}".format(self.item_type.name, self.price)
