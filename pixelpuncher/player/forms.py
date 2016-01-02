from datetime import datetime
from django import forms
from django.forms import model_to_dict

from pixelpuncher.game.utils import game_settings
from pixelpuncher.game.utils.skills import add_starting_skills
from pixelpuncher.player.models import Player, Occupation


class PlayerForm(forms.Form):
    name = forms.CharField(required=True, max_length=25, widget=forms.TextInput())
    previous_occupation = forms.ModelChoiceField(queryset=Occupation.objects.filter(active=True))

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

        occupation = data.get("previous_occupation")
        player.previous_occupation = occupation.name

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

        add_starting_skills(player)

        return player


class AttributeForm(forms.Form):
    power = forms.IntegerField(required=True, widget=forms.TextInput())
    technique = forms.IntegerField(required=True, widget=forms.TextInput())
    endurance = forms.IntegerField(required=True, widget=forms.TextInput())

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        self.user = kwargs.pop("user", None)
        self.ap_used = 0

        super(AttributeForm, self).__init__(*args, **kwargs)

        if self.instance:
            self.initial = model_to_dict(self.instance)

    def clean_power(self):
        clean_power = self.cleaned_data.get("power")

        if clean_power < self.instance.power:
            raise forms.ValidationError("Power cannot be less than previous value.")

        return clean_power

    def clean_technique(self):
        clean_technique = self.cleaned_data.get("technique")

        if clean_technique < self.instance.technique:
            raise forms.ValidationError("Technique cannot be less than previous value.")

        return clean_technique

    def clean_endurance(self):
        clean_endurance = self.cleaned_data.get("endurance")

        if clean_endurance < self.instance.endurance:
            raise forms.ValidationError("Endurance cannot be less than previous value.")

        return clean_endurance

    def clean(self):
        cleaned_data = super(AttributeForm, self).clean()
        current_points = self.instance.power + self.instance.endurance + self.instance.technique
        maximum_points = current_points + self.instance.attribute_points
        total_points = cleaned_data.get("power") + cleaned_data.get("technique") + cleaned_data.get("endurance")

        self.ap_used = total_points - current_points

        if total_points > maximum_points:
            raise forms.ValidationError("Too many points assigned!")

        return cleaned_data

    def save(self):
        data = self.cleaned_data
        player = self.instance

        player.power = data.get("power")
        player.technique = data.get("technique")
        player.endurance = data.get("endurance")

        player.attribute_points -= self.ap_used

        player.save()

        return player
