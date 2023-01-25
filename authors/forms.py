from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import re


# FORMS MANAGES ALL FIELDS THAT WILL BE SHOWED on HTML, clear means verify
def add_attr(field, attr_name, attr_new_value):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing}{attr_new_value}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)
    # field.widget.attrs['placeholder'] = placeholder_val


def password_validator(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError('A senha é invalida, deve conter letras maiusculas e minusculas alem de numeros'
                              , code='invalid')


def name_validator(name):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~ :]')
    if regex.match(name):
        raise ValidationError("Somente letras e numeros são permitidos", code='invalid')

    if " " in name:
        raise ValidationError("Somente o primeiro nome nesse campo", code='invalid')


def username_validator(username):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])$')
    if regex.match(username):
        raise ValidationError("Somente letras e numeros são permitidos", code='invalid')

    if " " in username:
        raise ValidationError("Somente o um nome nesse campo", code='invalid')


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

    # def clean_firld(self): VALIDATE JUST ONE FILD
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
