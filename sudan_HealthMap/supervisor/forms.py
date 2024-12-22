from django import forms
from state.models import State

class HospitalAccountForm(forms.Form):
    name = forms.CharField(max_length=255, label="Hospital Name")
    state = forms.ModelChoiceField(queryset=State.objects.all(),
        label="State",
        empty_label="Select a State")
    username = forms.CharField(max_length=150, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
