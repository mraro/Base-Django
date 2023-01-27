
from django import forms
from django.contrib.auth.models import User

# import re

from forms.django_forms import *


class RegisterForm(forms.ModelForm):  # HERE WE CAN OVERWRITE THE FILDS AND ADAPTATE THE form HE HAS A DEFAULT
    # FOR EVERY FIELDS
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu Nome')
        # add_attr(self.fields['username'], 'placeholder', 'Give me your name')
        add_placeholder(self.fields['email'], 'Seu e-mail')
        add_placeholder(self.fields['first_name'], 'Primeiro nome')
        add_placeholder(self.fields['last_name'], 'Sobrenome')
        # add_attr(self.fields['username'], 'min_length', '3')

    first_name = forms.CharField(validators=[name_validator],
                                 min_length=4,
                                 max_length=150)
    last_name = forms.CharField(validators=[name_validator],
                                min_length=4,
                                max_length=150)
    username = forms.CharField(min_length=4,
                               max_length=150)  # THIS WORKS BETTER THAN add_attr(self.fields['username'], 'min_length', '3')
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Sua senha',
        }),
        error_messages={
            'required': 'A senha não pode ser vazia'
        },
        validators=[password_validator],
        help_text=(
            '''A senha deve conter caracters especiais, letra maiuscula e minuscula com numeros,
            com pelo menos 8 caracters'''
        )
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repetir a senha'
        }),
        error_messages={
            'required': 'A senha não pode ser vazia'
        },
        label='Repetir senha'

    )
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')  # THIS CLEANED_DATA WAS CHECKED BY DJANGO
        # data = self.clean # THIS IS DIRECT WITHOUT DJANGO VALIDATOR
        if 'Alessandro' in data:
            raise ValidationError(
                'Nome em uso %(value)s ',
                code='invalid',
                params={'value': 'Alessandro'}
            )
        return data

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError("Email já em uso")
        return email

    def clean(self):  # DEFINED IN SUPER CLASS
        data_cleaned = super().clean()
        password = data_cleaned.get('password')  # GET VALUES FROM INPUT VALIDATION
        password2 = data_cleaned.get('password2')

        if password != password2:
            raise ValidationError({
                'password2': 'As senhas são divergentes'  # SET MESSAGE AND WHERE SHOULD SHOW

            },
                code='invalid'
            )  # IT'S POSSIBLE SEND A LIST OF PROBLEMS

    # HERE WE CAN OVERWRITE THE FILDS AND ADAPTATE  # THIS IS AN EXAMPLE WAY TO DO WHAT IT DID ABOVE
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
        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'E-mail',
            'password': 'Password',
        }
        help_texts = {
            'email': 'Ex: mail@mail.com',
        }
        error_messages = {
            'username': {
                'required': 'não pode ser vazio',
            }
        }

    #     widgets = {
    #         'first_name': forms.CharField(attrs={'placeholder': 'Seu Usuário', # ATTRIBUTES HTML
    #                                            'class': 'text-input-class',
    #                                            }),
    #
    #     }


