from collections import defaultdict

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.db.models import F, Value
from django.db.models.functions import Concat

from tags.models import TAG


# Create your models here.
# MODELS ARE DATABASE MODEL, HE MAKES CHANGES ON ANY DATABASE THAT IS SET UP HERE

class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name  # !IMPORTANT ISSO FARA COM QUE NO ADMIN DO DJANGO RETORNE O NOME DO OBJETO


class Manager(models.Manager):
    """ CAN I USE THIS IN A VIEW, IN THIS CASE TESTS IF IS PUBLISHED """

    @staticmethod
    def get_published():
        return Remedios.objects.filter(is_published=True).order_by('-id').annotate(
            # GIVE MORE ONE VARIABLE INTO A LIST OF QUERYSET
            author_full_name=Concat(
                F('author__first_name'),
                Value(" "),
                F('author__last_name'),
            )
        ).select_related('author', 'category')  # THIS IMPROVE READ DATABASE (WORKS ON FOREIGN KEY)


class Remedios(models.Model):  # ISSO É UMA TABELA NO DJANGO
    objects = Manager()
    title = models.CharField(max_length=65)  # IS LIKE MYSQL VARCHAR(65)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    price = models.FloatField(default=1)
    quantity = models.IntegerField(default=0)
    preparetion_steps = models.TextField()
    preparetion_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='farmacia/covers/%Y/%m/%d/',
                              blank=True,
                              default='static/images/default.jpg')  # campo de imagem
    # (blank=True permite campo vazio, default é a imagem padrão caso não exista

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )  # FOREING KEY (CHAVE ESTRANGERIA COM A class Category) on_delete definira o campo como null para não perder os
    # links com demais informações
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )
    # GENERIC
    # tags = GenericRelation(
    #     TAG, related_query_name='Remedios'
    # )
    # MANY TO MANY
    tags = models.ManyToManyField(TAG)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # THIS IS SO IMPORTANT, THIS IS CALLED IN TEMPLATE HTML (HAS THIS IN remedio.html)
        return reverse('farmacia:remedio', args=(self.id,))

    def clean(self, *args, **kwargs):   # VALIDAÇÃO GLOBAL | GLOBAL VALIDATION                  !IMPORTANT
        error_messages = defaultdict(list)

        remedio_from_db = Remedios.objects.filter(title__iexact=self.title).first()

        if remedio_from_db and remedio_from_db.pk != self.pk:
            error_messages['title'].append("Esse titulo já existe")

        if error_messages:
            raise ValidationError(error_messages)

    '''  THIS IS AN EXAMPLE TO REWRITE A BUILTIN METHOD
    I WONT USE THIS BECAUSE A HAD PUT A FUNC TO DO THE SAME THING IN clean_slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugfy(self.title)}'
            self.slug = slug
        return super().save(*args, **kwargs)
    '''
