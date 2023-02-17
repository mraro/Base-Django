from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name  # !IMPORTANT ISSO FARA COM QUE NO ADMIN DO DJANGO RETORNE O NOME DO OBJETO


class Remedios(models.Model):  # ISSO É UMA TABELA NO DJANGO

    title = models.CharField(max_length=65)  # IS LIKE MYSQL VARCHAR(65)
    description = models.TextField()
    slug = models.SlugField(unique=True)
    # preparation_time = models.IntegerField()
    # preparation_time_unit = models.CharField(max_length=65)
    # servings = models.IntegerField()
    # servings_unit = models.CharField(max_length=65)
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
    )  # FOREING KEY (CHAVE ESTRANGERIA COM A claa Category) on_delete definira o campo como null para não perder os
    # links com demais informações
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('farmacia:remedio', args=(self.id,))


    '''  THIS IS AN EXAMPLE TO REWRITE A BUILTIN METHOD
    I WONT USE THIS BECAUSE A HAD PUT A FUNC TO DO THE SAME THING IN clean_slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugfy(self.title)}'
            self.slug = slug
        return super().save(*args, **kwargs)
    '''
