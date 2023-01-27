import re
from django.core.exceptions import ValidationError


# # VALIDATORS::
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

    # def clean_field(self): VALIDATE JUST ONE FILD
