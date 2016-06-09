from __future__ import division

from django.db import models
from django_extensions.db import fields

from pixelpuncher.game.utils import game_settings
from pixelpuncher.users.models import User


VICTORY = 'v'
COMBAT = 'c'
PASSIVE = 'p'

GENDER = (
    ("M", "Male",),
    ("F", "Female",),
)

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

LAYER_TYPES = (
    ("body", "Body",),
    ("hair", "Hair",),
    ("face", "Face",),
    ("shirt", "Shirt",),
)

UNLOCK_METHODS = (
    ("start", "Starter",),
    ("discvr", "Discover",),
    ("purcha", "Purchase",),
    ("secret", "Secret",),
)


class Occupation(models.Model):
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


# TODO: Remove this model
class Avatar(models.Model):
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, default="M", choices=GENDER)
    image_path = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.image_path


class Player(models.Model):
    user = models.ForeignKey(User, related_name="player")
    name = models.CharField(max_length=25)
    gender = models.CharField(max_length=1, default="M", choices=GENDER)
    title = models.CharField(max_length=30, null=True, blank=True)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    punches = models.IntegerField(default=0)  # Number of Actions or turns
    avatar = models.ForeignKey(Avatar, null=True, blank=True)

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

    attribute_points = models.IntegerField(default=0)
    status = models.CharField(max_length=1, choices=PLAYER_STATUS, default=PASSIVE)

    head = models.ForeignKey('item.Item', null=True, blank=True, related_name="+", on_delete=models.SET_NULL)
    gloves = models.ForeignKey('item.Item', null=True, blank=True, related_name="+", on_delete=models.SET_NULL)
    torso = models.ForeignKey('item.Item', null=True, blank=True, related_name="+", on_delete=models.SET_NULL)

    motto = models.CharField(max_length=200, null=True, blank=True)
    previous_occupation = models.CharField(max_length=50, null=True, blank=True)

    pixels = models.IntegerField(default=0)

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

    def adjust_to_max_health(self):
        self.current_health = self.total_health

        return "Your health is fully restored."

    def adjust_energy(self, amount):
        self.current_energy += amount

        if self.current_energy < 0:
            self.current_energy = 0

        if self.current_energy > self.total_energy:
            self.current_energy = self.total_energy

        result = "You {0} <span class='energy'>{1} energy</span>.".format(
            "gain" if amount > 0 else "lose", abs(amount))

        return result

    def adjust_to_max_energy(self):
        self.current_energy = self.total_energy

        return "Your energy is fully restored."

    @property
    def health_percentage(self):
        return (self.current_health / self.total_health) * 100

    @property
    def energy_percentage(self):
        return (self.current_energy / self.total_energy) * 100

    @property
    def xp_to_next_level(self):
        return int(game_settings.XP_BASE_AMOUNT * (self.level * (self.level + 1)) / 2)

    @property
    def percentage_to_next_level(self):
        return (self.xp / self.xp_to_next_level) * 100

    @property
    def effect_power(self):
        bonus = 0

        if self.gloves:
            bonus += self.gloves.item_type.power_bonus

        if self.head:
            bonus += self.head.item_type.power_bonus

        if self.torso:
            bonus += self.torso.item_type.power_bonus

        return self.power + bonus

    @property
    def effect_technique(self):
        bonus = 0

        if self.gloves:
            bonus += self.gloves.item_type.technique_bonus

        if self.head:
            bonus += self.head.item_type.technique_bonus

        if self.torso:
            bonus += self.torso.item_type.technique_bonus

        return self.technique + bonus

    @property
    def effect_endurance(self):
        bonus = 0

        if self.gloves:
            bonus += self.gloves.item_type.endurance_bonus

        if self.head:
            bonus += self.head.item_type.endurance_bonus

        if self.torso:
            bonus += self.torso.item_type.endurance_bonus

        return self.endurance + bonus

    @property
    def effective_armor(self):
        armor_rating = 0

        if self.gloves:
            armor_rating += self.gloves.item_type.armor_rating

        if self.head:
            armor_rating += self.head.item_type.armor_rating

        if self.torso:
            armor_rating += self.torso.item_type.armor_rating

        return armor_rating

    @property
    def body_layer(self):
        layers = self.layers.filter(layer__layer_type='body', current=True)
        if layers.exists():
            return layers[0]
        else:
            return None

    @property
    def hair_layer(self):
        layers = self.layers.filter(layer__layer_type='hair', current=True)
        if layers.exists():
            return layers[0]
        else:
            return None

    @property
    def face_layer(self):
        layers = self.layers.filter(layer__layer_type='face', current=True)
        if layers.exists():
            return layers[0]
        else:
            return None

    @property
    def shirt_layer(self):
        layers = self.layers.filter(layer__layer_type='shirt', current=True)
        if layers.exists():
            return layers[0]
        else:
            return None


class AvatarLayer(models.Model):
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, default="M", choices=GENDER)
    image_path = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    layer_type = models.CharField(max_length=5, choices=LAYER_TYPES, default='body')
    unlock_method = models.CharField(max_length=6, choices=UNLOCK_METHODS, default="discov")

    def __unicode__(self):
        return self.image_path


class PlayerAvatar(models.Model):
    player = models.ForeignKey(Player, related_name="layers")
    layer = models.ForeignKey(AvatarLayer, related_name="+")
    current = models.BooleanField(default=False)


class Skill(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField()
    skill_type = models.CharField(max_length=4, choices=SKILL_TYPE)
    level = models.IntegerField(default=1)

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
    gained_bonus = models.IntegerField(default=0)  # how much bonus damage increases on level up

    date_created = fields.CreationDateTimeField(editable=True)
    date_updated = fields.ModificationDateTimeField(editable=True)

    def __unicode__(self):
        return self.name


class PlayerSkill(models.Model):
    player = models.ForeignKey(Player, related_name="skills")
    skill = models.ForeignKey(Skill, related_name="+")
    level = models.IntegerField(default=1)  # all skills start at level 1 and gain level when character levels
    remaining_for_level_up = models.IntegerField(default=1)  # levels until skill will increase

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

    def display_damage(self):
        if self.bonus > 0:
            return "{0}d{1} + {2}".format(self.number_of_dice, self.dice_sides, self.bonus)
        else:
            return "{0}d{1}".format(self.number_of_dice, self.dice_sides)

    @property
    def can_use(self):
        return self.player.current_energy >= self.skill.energy_cost
