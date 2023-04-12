from collections import defaultdict

from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _  # TRANSLATE as _
from django.contrib.auth.models import User

from farmacia.models import Remedios, Category
from forms.django_forms import name_validator, password_validator
from tags.models import TAG
from utility.remediosautofill import slugify


# serializer server to transform queryset in json api (here appears with models, but he gets by models to use here)
# serializer serve para transformar o queryset em json para api     # noqa
class TAG_Serializer(serializers.Serializer):  # noqa
    id = serializers.IntegerField()
    slug = serializers.SlugField()
    name = serializers.CharField(max_length=255)


class User_Serializer(serializers.Serializer):  # noqa
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()


class Remedio_Serializer(serializers.ModelSerializer):  # noqa

    class Meta:
        model = Remedios
        exclude = ['preparetion_steps', 'is_published', 'author',
                   'category']  # put all field or exclude someone (all fields include what is doing under)

    id = serializers.IntegerField(read_only=True, )
    link_remedio = serializers.HyperlinkedIdentityField(
        source='pk',
        view_name='farmacia:remedio_rest',
        # tem que passar o lookup_field, caso contrario não encontrará o campo # noqa
    )
    title = serializers.CharField(read_only=True, max_length=65)
    description = serializers.CharField(read_only=True, )
    slug = serializers.SlugField(read_only=True, )
    price = serializers.FloatField(read_only=True, default=1)
    quantity = serializers.IntegerField(read_only=True, default=0)
    created_at = serializers.DateTimeField(read_only=True, )
    update_at = serializers.DateTimeField(read_only=True, )
    ### THIS MAKE AN ESPECIAL FIELD:   # noqa
    modified = serializers.SerializerMethodField(
        read_only=True, )  # posso trocar o nome do methodo com method_name="" default é com get no começo # noqa

    def get_modified(self, remedios):  # noqa
        return f'{remedios.created_at} {remedios.update_at}'

    ### # noqa
    public = serializers.BooleanField(read_only=True, source='is_published')
    # aqui é um exemplo de como pegar uma chave estrangeira    # noqa
    foreign_category_pk = serializers.PrimaryKeyRelatedField(source='category', queryset='category')
    category_name = serializers.StringRelatedField(read_only=True, source='category')
    # aqui é como pega uma chave estrangeira a partir do model     # noqa
    author_pk = serializers.PrimaryKeyRelatedField(source='author', queryset=User.objects.all())
    author_name = serializers.StringRelatedField(source='author')
    author_full = User_Serializer(many=False, read_only=True, source='author')

    tags = serializers.PrimaryKeyRelatedField(queryset=TAG.objects.all(), many=True)
    tags_objects = TAG_Serializer(many=True, source='tags')
    # breakpoint()
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        view_name='farmacia:tag_rest',  # tem que passar o lookup_field, caso contrario não encontrará o campo # noqa
        lookup_field='slug',  # na url pede <slug:slug> # noqa
        read_only=True
    )

    # VALIDATE == validate:  > # authors/views/views_func/views_func_dashboard.py


class Dashboard_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Remedios  # database
        fields = 'id', 'title', 'price', 'quantity', 'description', 'cover', 'category_pk', 'category_name', 'slug', \
            # 'link_dashboard_remedio'
        # exclude = []

    id = serializers.IntegerField(read_only=True, )
    # link_dashboard_remedio = serializers.HyperlinkedIdentityField(source='id', view_name='authors:edit_rest')
    title = serializers.CharField(min_length=4, max_length=65, label='Title')
    print(title)
    slug = serializers.HiddenField(default=slugify(str(title)))
    # TO DJANGO SEND FORM PROPERLY, IN ORDER TO MAKE A SLUGFY LATER, BEFORE SEND TO IS_VALID
    price = serializers.DecimalField(min_value=0.00, max_digits=4, decimal_places=2, label='Price')
    # category = serializers.StringRelatedField(queryset=Category.objects.all())
    category_name = serializers.StringRelatedField(read_only=True, source='category')
    category_pk = serializers.PrimaryKeyRelatedField(source='category', queryset=Category.objects.all(), required=False)

    def validate(self, values):
        # print("validate Slug")
        # title = values.get('title')
        data = slugify(str(values.get('title')))
        print("SLUG")
        while Remedios.objects.filter(slug=data).exists():
            data += "X"
            # THIS IS A DANGEROUS FORM TO GRANT THAT NEVER HAS SAME SLUG
            # raise ValidationError('My unique field should be unique.')
        values['slug'] = data
        return values

    # HERE WE CAN OVERWRITE THE FILDS AND ADAPTATE  # THIS IS AN EXAMPLE WAY TO DO WHAT IT DID ABOVE
    def validate_title(self, data):  # VALIDAÇÃO GLOBAL | GLOBAL VALIDATION                  !IMPORTANT
        error_messages = defaultdict(list)
        title = data
        exists = Remedios.objects.filter(title__iexact=title).exists()

        if exists:
            error_messages['title'].append("Esse titulo já existe")

        if error_messages:
            raise ValidationError(error_messages)
        return title



class Register_User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
        ]

    first_name = serializers.CharField(validators=[name_validator],
                                       min_length=4,
                                       max_length=150,
                                       label=_('First name'),
                                       )

    last_name = serializers.CharField(min_length=4,
                                      max_length=150,
                                      label=_('Last name'),
                                      )

    username = serializers.CharField(min_length=4,
                                     max_length=150,
                                     label=_('Username'),
                                     )  # THIS WORKS BETTER THAN add_attr(self.fields['username'],
    # 'min_length', '3')
    password = serializers.CharField(
        required=True,

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
    password2 = serializers.CharField(
        required=True,

        error_messages={
            'required': _("Pass can't be empty")
        },
        label=_('Repeat password')

    )
    email = serializers.EmailField(label='E-mail',
                                   help_text='Ex: mail@mail.com', )

    def validate_first_name(self, data):
        if 'root' in data:
            raise ValidationError(
                f'{_("Name already in use")}: %(value)s',
                code='invalid',
                params={'value': data}
            )
        return data

    def validate_username(self, data):
        exists = User.objects.filter(username=data).exists()

        if exists:
            raise ValidationError(
                f'{_("Name already in use")}: %(value)s',
                code='invalid',
                params={'value': data}
            )
        return data

    def validate_email(self, data):
        email = data
        exists = User.objects.filter(email=email).exists()
        if exists:
            raise ValidationError(_("Email already used"))
        return email

    def validate(self, values):  # DEFINED IN SUPER CLASS
        password = values.get('password')  # GET VALUES FROM INPUT VALIDATION
        password2 = values.get('password2')

        if password != password2:
            raise ValidationError({
                'password2': _('Passwords are different')  # SET MESSAGE AND WHERE SHOULD SHOW

            },
                code='invalid'
            )  # IT'S POSSIBLE SEND A LIST OF PROBLEMS
        del (values['password2'])
        return values


class Login_User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
