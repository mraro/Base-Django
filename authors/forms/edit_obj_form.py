# DOC https://docs.djangoproject.com/en/4.1/ref/forms/fields/
from django import forms
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _  # TRANSLATE as _

from farmacia.models import Remedios


class EditObjectForm(forms.ModelForm):
    """ can you pass args to fill the fields, a dict with same name key with (instance="dict") """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # to rewrite dad class and grandpa etc
        self.full_clean()
        # add_attr(self.fields.get('slug'), 'type', 'hidden')

    # cover = forms.ImageField(allow_empty_file=True)
    title = forms.CharField(min_length=4, max_length=65, label=_('Title'))
    slug = forms.CharField(widget=forms.HiddenInput(), empty_value=" ", label="")  # HERE I HAD TO GIVE SOME FAKE DATA
    # TO DJANGO SEND FORM PROPERLY, IN ORDER TO MAKE A SLUGFY LATER, BEFORE SEND TO IS_VALID
    price = forms.DecimalField(min_value=0.00, max_value=100000.00, decimal_places=2, label=_('Price'))

    def clean_slug(self):
        # print("Clean Slug")
        data = slugify(self.cleaned_data.get('title'))
        # exists = Remedios.objects.filter(slug=data).exists()

        while Remedios.objects.filter(slug=data).exists():
            data += "X"
            # THIS IS A DANGEROUS FORM TO GRANT THAT NEVER HAS SAME SLUG
            # raise ValidationError('My unique field should be unique.')
        return data

    class Meta:
        model = Remedios  # database
        fields = 'title', 'price', 'quantity', 'description', 'cover', 'category', 'slug',
        # exclude = []
        labels = {
            # 'title': 'Titulo: ',
            'description': _('Description: ') ,
            # 'price': 'Preço: ',
            'cover': '',
            'quantity': _('Quantity: '),
            'category': _('Category: '),

        }

        widgets = {

            'cover': forms.FileInput(
                attrs={
                    'class': 'image-object'
                }
            ),
            'quantity': forms.Select(attrs={'class': 'quantity-object'},
                                     choices=(
                                         ('0', '0'),
                                         ('30', '30'),
                                         ('60', '60'),
                                         ('120', '120'),
                                     )
                                     )
        }
