from django.db import models
from django_extensions.db import fields

from pixelpuncher.player.models import Player


class GameMessage(models.Model):
    player = models.ForeignKey(Player)
    message = models.TextField()
    shown = models.BooleanField(default=False)
    date_created = fields.CreationDateTimeField(editable=True)

    def __unicode__(self):
        return self.message
