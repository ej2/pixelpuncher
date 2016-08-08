from __future__ import division

from django.db import models

from pixelpuncher.item.models import ItemType
from pixelpuncher.player.models import GENDER, AvatarLayer, Player

TRIGGER_TYPE = (
    ("ASK", "Ask about",),
    ("TELL", "Tell about",),
    ("ACK", "Acknowledge",),
    ("GRT", "Greeting")
)

RELATIONSHIP_TYPE = (
    ('RIVL', 'Rival',),
    ('FRND', 'Friend',),
    ('CUST', 'Customer',),
    ('ROMC', 'Romantic',),
)

RELATIONSHIP_LEVEL = (
    ('BS', 'Best',),
    ('GD', 'Good',),
    ('NT', 'Netural',),
    ('BD', 'Bad',),
    ('HR', 'Horrible',),
)


class RelationshipLevels(object):
    BEST = 'BS'
    GOOD = 'GD'
    NETURAL = 'NT'
    BAD = 'BD'
    HORRIBLE = 'HR'


class Triggers(object):
    ASK = 'ask'
    TELL = 'tell'
    HELP = 'help'
    GREET = 'greet'
    ACKNOWLEDGE = 'ack'


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

    # Used when creating new relationships between NPC and player
    default_relationship_type = models.CharField(max_length=4, choices=RELATIONSHIP_TYPE, default='CUST')

    total_health = models.IntegerField(default=10)
    total_energy = models.IntegerField(default=10)

    power = models.IntegerField(default=1)
    technique = models.IntegerField(default=1)
    endurance = models.IntegerField(default=1)

    avatar = models.ForeignKey(NPCAvatar, null=True, blank=True)

    def __unicode__(self):
        return self.name


class NPCRelationship(models.Model):
    npc = models.ForeignKey(NPC, related_name="+")
    player = models.ForeignKey(Player, related_name="npcs")

    # Type and level determine how npc treats player
    # Score determines how close level is to going up or down.
    score = models.IntegerField(default=0)
    relationship_type = models.CharField(max_length=4, choices=RELATIONSHIP_TYPE)
    relationship_level = models.CharField(max_length=4, choices=RELATIONSHIP_LEVEL, default='NT')

    current_health = models.IntegerField(default=10)
    current_energy = models.IntegerField(default=10)
    pixels = models.IntegerField(default=0)

    avatar = models.ForeignKey(NPCAvatar, null=True, blank=True)

    def __unicode__(self):
        return self.npc.name


class Response(models.Model):
    text = models.TextField()
    health_change = models.IntegerField(default=0)
    energy_change = models.IntegerField(default=0)
    pixels_change = models.IntegerField(default=0)
    xp_change = models.IntegerField(default=0)
    reward_items = models.ManyToManyField(ItemType, related_name="+", blank=True)
    relationship_points = models.IntegerField(default=0)

    priority = models.IntegerField(default=0)  # determines which response to give first
    frequency = models.IntegerField(default=0)  # how often response can be given in minutes
    # Frequency options: timed, no limit, max number (n times)

    level_requirement = models.IntegerField(default=0)  # zero means no requirement
    required_items = models.ManyToManyField(ItemType, related_name="+", blank=True)

    def __unicode__(self):
        return self.text


class ResponseTrigger(models.Model):
    npcs = models.ManyToManyField(NPC, related_name="triggers")
    response = models.ForeignKey(Response, related_name="triggers")
    trigger_text = models.CharField(max_length=30)
    trigger_type = models.CharField(max_length=4, choices=TRIGGER_TYPE)

    def __unicode__(self):
        return self.trigger_text


class ResponseLog(models.Model):
    # Track responses given to player by NPCs
    player = models.ForeignKey(Player, related_name="+")
    response = models.ForeignKey(Response, related_name="+")
    response_trigger = models.ForeignKey(ResponseTrigger, related_name="+")
    response_date = models.DateTimeField()
