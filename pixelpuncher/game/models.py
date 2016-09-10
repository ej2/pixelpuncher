from django.db import models
from django_extensions.db import fields

from pixelpuncher.player.models import Player


class GameState(object):
    PLAY = 'PLAY'
    GAME_OVER = 'OVER'
    CLOSED = 'CLSD'

    STATE = (
        ('PLAY', 'Playing',),
        ('OVER', 'Game Over',),
        ('CLSD', 'Closed',),
    )


class CardType(object):
    BOMB = 'B'
    ONE = '1'
    TWO = '2'
    FOUR = '4'
    EIGHT = '8'
    SPECIAL = 'S'

    CARDS = (
        ('B', 'Bomb'),
        ('1', 'One'),
        ('2', 'Two'),
        ('4', 'Four'),
        ('8', 'Eight'),
        ('S', 'Special'),
    )


class GameMessage(models.Model):
    player = models.ForeignKey(Player)
    message = models.TextField()
    shown = models.BooleanField(default=False)
    date_created = fields.CreationDateTimeField(editable=True)

    def __unicode__(self):
        return self.message


class MatchGame(models.Model):
    player = models.ForeignKey(Player)
    date_created = fields.CreationDateTimeField(editable=True)
    state = models.CharField(max_length=4, choices=GameState.STATE, default='PLAY')
    points = models.IntegerField(default=0)
    multiplier = models.IntegerField(default=1)


class MatchCard(models.Model):
    game = models.ForeignKey(MatchGame, related_name='cards')
    card_type = models.CharField(max_length=1, choices=CardType.CARDS)
    flipped = models.BooleanField(default=False)
    position = models.IntegerField(default=0)

    @property
    def image(self):
        if self.flipped:
            return "images/cards/{}.png".format(self.card_type)
        else:
            return "images/cards/card_back.png"
