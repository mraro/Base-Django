from django.urls import reverse
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _  # TRANSLATE as _
from django.contrib.auth.models import User

from farmacia.models import Remedios
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

    # VALIDATE == CLEAN:  > # authors/views/views_func/views_func_dashboard.py


class Dashboard_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Remedios  # database
        fields = 'title', 'price', 'quantity', 'description', 'cover', 'category', 'slug', \
            # 'link_dashboard_remedio'
        # exclude = []

    # link_dashboard_remedio = serializers.HyperlinkedIdentityField(source='id', view_name='authors:edit_rest')
    title = serializers.CharField(min_length=4, max_length=65, label='Title')
    # TO DJANGO SEND FORM PROPERLY, IN ORDER TO MAKE A SLUGFY LATER, BEFORE SEND TO IS_VALID
    price = serializers.DecimalField(min_value=0.00, max_digits=4, decimal_places=2, label=_('Price'))

    # def validate(self, values):
    #     # print("Clean Slug")
    #     # title = values.get('title')
    #     data = slugify('Earum6')
    #
    #     while Remedios.objects.filter(slug=data).exists():
    #         data += "X"
    #         # THIS IS A DANGEROUS FORM TO GRANT THAT NEVER HAS SAME SLUG
    #         # raise ValidationError('My unique field should be unique.')
    #     return data
