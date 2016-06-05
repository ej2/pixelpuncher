import factory
from factory.django import DjangoModelFactory

from pixelpuncher.player.models import Player


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player

    name = "Test Location"
    #user = factory.SubFactory(UserFactory)
    gender = "M"
    title = "Title"
