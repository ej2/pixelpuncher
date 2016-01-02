from django.db import models
from django_extensions.db import fields

from pixelpuncher.item.models import DropTable
from pixelpuncher.player.models import Player


class EnemyCategory(models.Model):
    code = models.CharField(unique=True, primary_key=True, max_length=20)
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class EnemyType(models.Model):
    name = models.CharField(max_length=25)
    category = models.ForeignKey(EnemyCategory, related_name="+")
    minimum_health = models.IntegerField(default=1)
    maximum_health = models.IntegerField(default=1)
    xp = models.IntegerField(default=1)
    base_level = models.IntegerField(default=1)
    date_created = fields.CreationDateTimeField(editable=True)
    date_updated = fields.ModificationDateTimeField(editable=True)
    drop_table = models.ForeignKey(DropTable, related_name="+", null=True, blank=True)

    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)

    # For calculating damage
    number_of_dice = models.IntegerField(default=1)
    dice_sides = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)

    image_name = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Enemy(models.Model):
    enemy_type = models.ForeignKey(EnemyType, related_name="+")
    player = models.ForeignKey(Player, related_name="enemies")
    current_health = models.IntegerField(default=0)
    total_health = models.IntegerField(default=0)
    date_created = fields.CreationDateTimeField(editable=True)
    date_updated = fields.ModificationDateTimeField(editable=True)
    active = models.BooleanField(default=True)

    hits = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)

    # For calculating damage
    number_of_dice = models.IntegerField(default=1)
    dice_sides = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)

    class Meta:
        verbose_name = "enemy"
        verbose_name_plural = "enemies"

    def __unicode__(self):
        return self.enemy_type.name

    @property
    def is_defeated(self):
        if self.active is False or self.current_health <= 0:
            return True

        return False

    def adjust_health(self, amount):
        self.current_health += amount

        if self.current_health < 0:
            self.current_health = 0
            self.active = False

        if self.current_health > self.total_health:
            self.current_health = self.total_health
