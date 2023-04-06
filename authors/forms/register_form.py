from collections import defaultdict

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext as _  # TRANSLATE as _

from farmacia.models import Remedios
# import re

from forms.django_forms import *


class RegisterForm(forms.ModelForm):  # HERE WE CAN OVERWRITE THE FILDS AND ADAPTATE THE form HE HAS A DEFAULT
    # FOR EVERY FIELDS
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], _('Your name'))
        # add_attr(self.fields['username'], 'placeholder', 'Give me your name')
        add_placeholder(self.fields['email'], _('Your email'))
        add_placeholder(self.fields['first_name'], _('First Name'))
        add_placeholder(self.fields['last_name'], _('Last Name'))
        # add_attr(self.fields['username'], 'min_length', '3')

    first_name = forms.CharField(validators=[name_validator],
                                 min_length=4,
                                 max_length=150,
                                 label=_('First name'),
                                 )

    last_name = forms.CharField(min_length=4,
                                max_length=150,
                                label=_('Last name'),
                                )

    username = forms.CharField(min_length=4,
                               max_length=150,
                               label=_('Username'),
                               )  # THIS WORKS BETTER THAN add_attr(self.fields['username'],
    # 'min_length', '3')
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Your Password'),
        }),
        error_messages={
            'required': _("Pass can't be empty")
        },
        validators=[password_validator],
        help_text=(
            _('The password must contain special characters, uppercase and lowercase letters with numbers, '
              'with at least 8 characters')
            # noqa
        ),
        label=_('Password'),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': _('Repeat password')
        }),
        error_messages={
            'required': _("Pass can't be empty")
        },
        label=_('Repeat password')

    )
    email = forms.EmailField(label='E-mail',
                             help_text='Ex: mail@mail.com', )

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')  # THIS CLEANED_DATA WAS CHECKED BY DJANGO
        # data = self.clean # THIS IS DIRECT WITHOUT DJANGO VALIDATOR
        if 'root' in data:
            raise ValidationError(
                f'{_("Name already in use")}: %(value)s',
                code='invalid',
                params={'value': 'root'}
            )
        return data

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(_("Email already used"))
        return email

    def clean(self):  # DEFINED IN SUPER CLASS
        data_cleaned = super().clean()
        password = data_cleaned.get('password')  # GET VALUES FROM INPUT VALIDATION
        password2 = data_cleaned.get('password2')

        if password != password2:
            raise ValidationError({
                'password2': _('Passwords are different')  # SET MESSAGE AND WHERE SHOULD SHOW

            },
                code='invalid'
            )  # IT'S POSSIBLE SEND A LIST OF PROBLEMS

    # HERE WE CAN OVERWRITE THE FILDS AND ADAPTATE  # THIS IS AN EXAMPLE WAY TO DO WHAT IT DID ABOVE
    def clean_title(self, *args, **kwargs):  # VALIDAÇÃO GLOBAL | GLOBAL VALIDATION                  !IMPORTANT
        error_messages = defaultdict(list)
        title = self.cleaned_data.get('title')
        exists = Remedios.objects.filter(title__iexact=title).exists()

        if exists:
            error_messages['title'].append("Esse titulo já existe")

        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]
        # exclude = ['first_name']
        # labels = {    # deactivate by fail, can't translate here, will be done above
        #     'username': _('Username'),
        #     'first_name': _('First name'),
        #     'last_name': _('Last name'),
        #     'email': _('E-mail'),
        #     'password': _('Password'),
        # }
        # help_texts = {    # fail
        #     'email': 'Ex: mail@mail.com',
        # }
        error_messages = {
            'username': {
                'required': _("Can't be empty"),
            }
        }

    #     widgets = {
    #         'first_name': forms.CharField(attrs={'placeholder': 'Seu Usuário', # ATTRIBUTES HTML
    #                                            'class': 'text-input-class',
    #                                            }),
    #
    #     }
