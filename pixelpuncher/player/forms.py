from datetime import datetime
from django import forms
from django.forms import model_to_dict

from pixelpuncher.game.utils import game_settings
from pixelpuncher.player.models import Player


class PlayerForm(forms.Form):
    name = forms.CharField(required=True, max_length=25, widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        self.user = kwargs.pop("user", None)

        super(PlayerForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.initial = model_to_dict(self.instance)

    def save(self):
        data = self.cleaned_data

        player = Player()
        player.user = self.user

        player.name = data.get("name")
        player.total_health = game_settings.BASE_HEALTH
        player.current_health = game_settings.BASE_HEALTH

        player.total_energy = game_settings.BASE_ENERGY
        player.current_energy = game_settings.BASE_ENERGY

        player.punches = game_settings.DAILY_PUNCHES

        player.power = game_settings.BASE_POWER
        player.technique = game_settings.BASE_TECHNIQUE
        player.endurance = game_settings.BASE_ENDURANCE

        player.date_last_punch_reset = datetime.now()
        player.save()

        return player
