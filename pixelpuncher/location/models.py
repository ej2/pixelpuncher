from __future__ import division
from django.db import models
from django_extensions.db import fields

from pixelpuncher.item.models import ItemType
from pixelpuncher.npc.models import NPC
from pixelpuncher.player.models import Player


LOCATION_TYPE = (
    ("ADV", "Adventure",),
    ("MED", "Medical",),
    ("SHP", "Shop",),
    ("PWN", "Pawn",),
    ("CAS", "Casino",),
    ("TRN", "Training",),
    ("HOM", "Home",),
)

SERVICE_TYPE = (
    ("HEAL", "Healing",),
    ("REST", "Rest",),
    ("HEALMAX", "Restore Health",),
    ("RESTMAX", "Restore Energy",),
    ("GMB", "Gambling",),
    ("PICK4", "Pick 4",),
)

CURRENCY = (
    ("P", "Pixels",),
    ("M", "MegaPixels",),
)

SUCCESS_BONUS_STAT = (
    ("POWR", "power",),
    ("TECH", "technique",),
    ("ENDR", "endurance",),
    ("ARMR", "armor",),
)

ENCOUNTER_FREQUENCY = (
    ("COMMON", "Common",),
    ("RARE", "Rare",),
    ("ULTRA", "Ultra Rare",),
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
    adventure_rate = models.IntegerField(default=50)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.name


class LocationItem(models.Model):
    location = models.ForeignKey(Location, related_name="items")
    item_type = models.ForeignKey(ItemType)
    price = models.IntegerField()
    currency = models.CharField(max_length=1, choices=CURRENCY, default='P')

    def __unicode__(self):
        return "{} ${}".format(self.item_type.name, self.price)


class Service(models.Model):
    name = models.CharField(max_length=20)
    service_type = models.CharField(max_length=7, choices=SERVICE_TYPE)
    icon = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    min_amount = models.IntegerField(default=1)
    max_amount = models.IntegerField(default=1)
    success_rate = models.IntegerField(default=100)
    success_text = models.CharField(max_length=200)
    failure_text = models.CharField(max_length=200)
    page = models.CharField(max_length=200, null=True, blank=True)  # page to load if servicee requires it

    def __unicode__(self):
        return self.name


class LocationService(models.Model):
    service = models.ForeignKey(Service, related_name="locations")
    location = models.ForeignKey(Location, related_name="services")
    price = models.IntegerField()
    action_point_cost = models.IntegerField(default=0)

    def __unicode__(self):
        return "{}".format(self.service.name)


class Adventure(models.Model):
    title = models.CharField(max_length=30)
    image_path = models.CharField(max_length=200, null=True, blank=True)
    adventure_text = models.TextField()
    location = models.ManyToManyField(Location, related_name="adventures", blank=True)
    frequency = models.CharField(max_length=6, choices=ENCOUNTER_FREQUENCY)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title


class AdventureChoice(models.Model):
    adventure = models.ForeignKey(Adventure, related_name="choices")
    # Used if this choice leads to another adventure
    follow_up_adventure = models.ForeignKey(Adventure, related_name="+", null=True, blank=True)
    option_text = models.CharField(max_length=50)
    icon = models.CharField(max_length=20, blank=True, null=True)
    success_percentage = models.IntegerField(default=100)
    success_bonus = models.CharField(max_length=4, choices=SUCCESS_BONUS_STAT, null=True, blank=True)
    success_text = models.TextField()
    failure_text = models.TextField(blank=True, null=True)

    health_change = models.IntegerField(default=0)
    energy_change = models.IntegerField(default=0)
    pixels_change = models.IntegerField(default=0)
    xp_change = models.IntegerField(default=0)

    reward_items = models.ManyToManyField(ItemType, related_name="+", blank=True)

    def __unicode__(self):
        return self.option_text


class PlayerAdventure(models.Model):
    adventure = models.ForeignKey(Adventure, related_name="+")
    player = models.ForeignKey(Player, related_name="+")
    choice_made = models.ForeignKey(AdventureChoice, related_name="+", null=True, blank=True)
    active = models.BooleanField(default=True)
    date_created = fields.CreationDateTimeField(editable=True)
    date_updated = fields.ModificationDateTimeField(editable=True)
