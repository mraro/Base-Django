from django.forms import CharField
from django import forms

from forms.django_forms import add_placeholder


class LoginForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Type your username')
        add_placeholder(self.fields['password'], 'Type your password')
        print(self.cleaned_data.get('username'))
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
