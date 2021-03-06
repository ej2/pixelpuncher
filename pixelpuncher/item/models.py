from __future__ import division

from django.db import models
from django_extensions.db import fields

from pixelpuncher.player.models import Player, AvatarLayer

BASE_TYPE = (
    ("WEA", "Weapon",),
    ("ARM", "Armor",),
    ("CON", "Consumable",),
    ("UNL", "Unlock",),
    ("JNK", "Junk",),
)

CLASSIFICATION = (
    ("DRINK", "Drink",),
    ("FOOD", "Food",),
    ("GLOVE", "Gloves",),
    ("HAIR", "Hair",),
    ("HEAD", "Head",),
    ("MISC", "Misc",),
    ("SHIRT", "Shirt",),
    ("TORSO", "Torso",),
)


class Container(models.Model):
    name = models.CharField(max_length=40)  # Examples: Crate, Fridge, Chest, Closet, Trash Can
    description = models.CharField(max_length=500, null=True, blank=True)
    icon = models.CharField(max_length=30, null=True, blank=True)
    action = models.CharField(max_length=30, null=True, blank=True)
    location = models.ForeignKey('location.Location', related_name="containers")

    def __unicode__(self):
        return self.name


class PlayerContainer(models.Model):
    container = models.ForeignKey(Container, related_name="player_containers")
    player = models.ForeignKey(Player, related_name="+")

    class Meta:
        unique_together = ('container', 'player',)

    def __unicode__(self):
        return "{}'s {}".format(self.player.name, self.container.name)


class ItemType(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)
    base_type = models.CharField(max_length=3, choices=BASE_TYPE)
    classification = models.CharField(max_length=6, choices=CLASSIFICATION)
    total_uses = models.IntegerField(default=0)

    min_damage = models.IntegerField(default=0)
    max_damage = models.IntegerField(default=0)

    armor_rating = models.IntegerField(default=0)
    power_bonus = models.IntegerField(default=0)
    technique_bonus = models.IntegerField(default=0)
    endurance_bonus = models.IntegerField(default=0)
    xp_bonus = models.IntegerField(default=0)

    total_health_bonus = models.IntegerField(default=0)
    total_energy_bonus = models.IntegerField(default=0)

    current_health_bonus = models.IntegerField(default=0)
    current_energy_bonus = models.IntegerField(default=0)

    action_verb = models.CharField(max_length=30, null=True, blank=True)
    stackable = models.BooleanField(default=False)
    level_requirement = models.IntegerField(default=1)

    icon = models.CharField(max_length=30, null=True, blank=True)
    combat_usable = models.BooleanField(default=False)

    # This layer is unlocked when item is acquired
    layer = models.ForeignKey(AvatarLayer, related_name="+", null=True, blank=True)

    sellable = models.BooleanField(default=True)
    sell_price = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return "{0} ({1})".format(self.name, self.level_requirement)


class Item(models.Model):
    player = models.ForeignKey(Player, related_name="items", null=True, blank=True, on_delete=models.SET_NULL)
    item_type = models.ForeignKey(ItemType, related_name="+", default=None, null=True)
    remaining_uses = models.IntegerField(default=0)
    date_created = fields.CreationDateTimeField(editable=True)
    date_updated = fields.ModificationDateTimeField(editable=True)
    container = models.ForeignKey(PlayerContainer, related_name="items", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['item_type__name']

    def __unicode__(self):
        return self.item_type.name

    @property
    def name(self):
        if self.item_type.stackable:
            return "{} (x{})".format(self.item_type.name, self.remaining_uses)
        else:
            return self.item_type.name

    @property
    def display_verb(self):
        verb = self.item_type.action_verb or "use"
        return verb


class DropTable(models.Model):
    name = models.CharField(max_length=30)
    max_rate = models.IntegerField(default=100)
    max_drops = models.IntegerField(default=1)
    recommended_level = models.IntegerField(default=1)  # mainly used to automate creation of item drops

    def __unicode__(self):
        return self.name


class ItemDrop(models.Model):
    drop_table = models.ForeignKey(DropTable, related_name="items")
    item_type = models.ForeignKey(ItemType, related_name="+")
    drop_rate = models.IntegerField()  # From 0 to 1000


class LevelEquipment(models.Model):
    item_type = models.ForeignKey(ItemType, related_name="+")
    level = models.IntegerField(default=1)

