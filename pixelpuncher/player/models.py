from __future__ import division

from django.db import models
from django_extensions.db import fields

from pixelpuncher.users.models import User


VICTORY = 'v'
COMBAT = 'c'
PASSIVE = 'p'

PLAYER_STATUS = (
    ("p", "Passive",),
    ("c", "Combat",),
    ("v", "Victory",),
)

SPECIAL_TYPES = (
    ("energygain", "Energy Gain",),
    ("healthgain", "Health Gain",),
)

SKILL_TYPE = (
    ("ATTK", "Attack",),
    ("SPCL", "Special",),
    ("HEAL", "Heal",),
)


class Player(models.Model):
    user = models.ForeignKey(User, related_name="player")
    name = models.CharField(max_length=25)
    title = models.CharField(max_length=30)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    punches = models.IntegerField(default=0)  # Number of Actions or turns

    total_health = models.IntegerField(default=1)
    current_health = models.IntegerField(default=1)

    total_energy = models.IntegerField(default=1)
    current_energy = models.IntegerField(default=1)

    date_created = fields.CreationDateTimeField(editable=True)
    date_updated = fields.ModificationDateTimeField(editable=True)
    date_last_login = models.DateTimeField(null=True, blank=True)
    date_last_punch_reset = models.DateTimeField(null=True, blank=True)

    power = models.IntegerField(default=1)
    technique = models.IntegerField(default=1)
    endurance = models.IntegerField(default=1)

    status = models.CharField(max_length=1, choices=PLAYER_STATUS, default=PASSIVE)

    head = models.ForeignKey('item.Item', null=True, blank=True, related_name="+")
    gloves = models.ForeignKey('item.Item', null=True, blank=True, related_name="+")

    def __unicode__(self):
        return self.name

    def adjust_health(self, amount):
        self.current_health += amount

        if self.current_health < 0:
            self.current_health = 0

        if self.current_health > self.total_health:
            self.current_health = self.total_health

        result = "You {0} <span class='health'>{1} health</span>.".format(
            "gain" if amount > 0 else "lose", abs(amount))

        return result

    def adjust_energy(self, amount):
        self.current_energy += amount

        if self.current_energy < 0:
            self.current_energy = 0

        if self.current_energy > self.total_energy:
            self.current_energy = self.total_energy

        result = "You {0} <span class='energy'>{1} energy</span>.".format(
            "gain" if amount > 0 else "lose", abs(amount))

        return result

    @property
    def health_percentage(self):
        return (self.current_health / self.total_health) * 100

    @property
    def energy_percentage(self):
        return (self.current_energy / self.total_energy) * 100

    @property
    def effect_power(self):
        bonus = 0

        if self.gloves:
            bonus += self.gloves.item_type.power_bonus

        if self.head:
            bonus += self.head.item_type.power_bonus

        return self.power + bonus

    @property
    def effect_technique(self):
        bonus = 0

        if self.gloves:
            bonus += self.gloves.item_type.technique_bonus

        if self.head:
            bonus += self.head.item_type.technique_bonus

        return self.technique + bonus

    @property
    def effect_endurance(self):
        bonus = 0

        if self.gloves:
            bonus += self.gloves.item_type.endurance_bonus

        if self.head:
            bonus += self.head.item_type.endurance_bonus

        return self.endurance + bonus

    @property
    def effective_armor(self):
        # TODO: finish armor calculation
        return 0


class Skill(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    skill_type = models.CharField(max_length=4, choices=SKILL_TYPE)

    number_of_dice = models.IntegerField(default=1)
    dice_sides = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)

    hit_percentage = models.IntegerField(default=0)
    critical_percentage = models.IntegerField(default=0)
    critical_multipler = models.DecimalField(default=2.0, decimal_places=2, max_digits=4)
    energy_cost = models.IntegerField(default=0)

    special_type = models.CharField(max_length=12, choices=SPECIAL_TYPES, null=True, blank=True)  # Additional effects
    special_value_1 = models.IntegerField(default=0)  # to be used in special type action
    special_value_2 = models.IntegerField(default=0)
    special_value_3 = models.IntegerField(default=0)

    gain_frequency = models.IntegerField(default=1)  # how frequently skill improves in levels
    gained_hit = models.IntegerField(default=0)  # how much hit percentage increases on level up
    gained_critical = models.IntegerField(default=0)  # how much critical percentage increases on level up
    gained_critical_multipler = models.IntegerField(default=0)  # how much critical multipler increases on level up
    gained_energy_cost = models.IntegerField(default=0)  # how much energy cost increases on level up

    date_created = fields.CreationDateTimeField(editable=True)
    date_updated = fields.ModificationDateTimeField(editable=True)

    def __unicode__(self):
        return self.name


class PlayerSkill(models.Model):
    player = models.ForeignKey(Player, related_name="skills")
    skill = models.ForeignKey(Skill, related_name="+")
    level = models.IntegerField(default=1)  # all skills start at level 1 and gain level when character levels

    hit_percentage = models.IntegerField(default=0)
    critical_percentage = models.IntegerField(default=0)
    critical_multipler = models.DecimalField(default=2.0, decimal_places=2, max_digits=4)

    energy_cost = models.IntegerField(default=0)

    number_of_dice = models.IntegerField(default=0)
    dice_sides = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)

    date_created = fields.CreationDateTimeField(editable=True)
    date_updated = fields.ModificationDateTimeField(editable=True)

    def __unicode__(self):
        return self.skill.name
