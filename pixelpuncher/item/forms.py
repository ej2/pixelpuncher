from django import forms

from pixelpuncher.item.utils import put_item_in_container


class ContainerForm(forms.Form):
    items = forms.ModelChoiceField(queryset=None, required=True, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        self.player_container = kwargs.pop("player_container", None)

        super(ContainerForm, self).__init__(*args, **kwargs)
        self.fields["items"].label_from_instance = self.item_label
        self.fields["items"].queryset = self.player_container.player.items.all().order_by("item_type__name")

    def save(self):
        self.full_clean()
        data = self.cleaned_data
        item = data.get("items")
        result = put_item_in_container(item, self.player_container)

        return result

    @staticmethod
    def item_label(obj):
        if obj.item_type.stackable:
            return "{} (x{})".format(obj.item_type.name, obj.remaining_uses)
        else:
            return obj.item_type.name

