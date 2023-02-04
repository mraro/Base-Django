from django.forms import CharField
from django import forms

from forms.django_forms import add_placeholder
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['username'], 'Digite seu usuario')
        add_placeholder(self.fields['password'], 'Digite sua senha')

        self.full_clean()

    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )

