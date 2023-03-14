import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _  # TRANSLATE as _


# # VALIDATORS::
# FORMS MANAGES ALL FIELDS THAT WILL BE SHOWED on HTML, clear means verify
def add_attr(field, attr_name, attr_new_value):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing}{attr_new_value}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)
    # field.widget.attrs['placeholder'] = placeholder_val


def password_validator(password):
    msg_translated = _("Invalid password, use Upper and down case with numbers and especial characters")
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')  # noqa
    if not regex.match(password):
        raise ValidationError(msg_translated, code='invalid')


def name_validator(name):
    msg_translated_first_error = _('Just letters and numbers are allowed')
    msg_translated_sec_error = _('Only first name here')
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~ :]')  # noqa
    if regex.match(name):
        raise ValidationError(msg_translated_first_error, code='invalid')

    if " " in name:
        raise ValidationError(msg_translated_sec_error, code='invalid')

    # def clean_field(self): VALIDATE JUST ONE FILD
