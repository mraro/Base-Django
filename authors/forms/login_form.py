from django import forms
from django.utils.translation import gettext_lazy as _  # TRANSLATE as _

from forms.django_forms import add_placeholder, add_attr


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_placeholder(self.fields['username'], _('Type your username'))
        add_placeholder(self.fields['password'], _('Type your password'))
        self.full_clean()

    username = forms.CharField(label=_('Username'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(), )

