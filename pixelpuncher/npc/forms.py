from django import forms

from pixelpuncher.npc.models import NPCAvatar
from pixelpuncher.player.models import AvatarLayer


class CustomNPCAvatarForm(forms.ModelForm):
    class Meta:
        model = NPCAvatar
        fields = ['name', 'body_layer', 'hair_layer', 'face_layer', 'shirt_layer']

    def __init__(self, *args, **kwargs):
        super(CustomNPCAvatarForm, self).__init__(*args, **kwargs)

        self.fields['body_layer'].queryset = AvatarLayer.objects.filter(layer_type='body').order_by('name')
        self.fields['hair_layer'].queryset = AvatarLayer.objects.filter(layer_type='hair').order_by('name')
        self.fields['face_layer'].queryset = AvatarLayer.objects.filter(layer_type='face').order_by('name')
        self.fields['shirt_layer'].queryset = AvatarLayer.objects.filter(layer_type='shirt').order_by('name')

