from datetime import datetime
from django import forms
from django.forms import model_to_dict

from pixelpuncher.game.utils import game_settings
from pixelpuncher.game.utils.skills import add_starting_skills
from pixelpuncher.item.utils import give_level_equipment, auto_equip
from pixelpuncher.location.utils import assign_starting_locations
from pixelpuncher.player.models import Player, Occupation, GENDER, Avatar
from pixelpuncher.player.utils.avatar import generate_random_starting_avatar


class PlayerForm(forms.Form):
    name = forms.CharField(required=True, max_length=25, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(required=True, choices=GENDER, widget=forms.Select(attrs={'class': 'form-control'}))
    previous_occupation = forms.ModelChoiceField(
        queryset=Occupation.objects.filter(active=True), widget=forms.Select(attrs={'class': 'form-control'}))

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
        player.gender = data.get("gender")

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
        give_level_equipment(player)
        auto_equip(player)
        assign_starting_locations(player)
        generate_random_starting_avatar(player)

        return player


class AttributeForm(forms.Form):
    power = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"class": "form-attribute-field" }))
    technique = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"class": "form-attribute-field" }))
    endurance = forms.IntegerField(required=True, widget=forms.TextInput(attrs={"class": "form-attribute-field" }))

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
