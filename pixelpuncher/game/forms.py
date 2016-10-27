from django import forms


class CheatCodeForm(forms.Form):
    code = forms.CharField(required=True, max_length=64, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CheatCodeForm, self).__init__(*args, **kwargs)


