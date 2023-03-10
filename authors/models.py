from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Manager(models.Manager):
    ...


class Profile(models.Model):
    objects = Manager()
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)
    # AQUI TEMOS UMA CHAVE ESTRANGEIRA QUE SERÁ MODIFICADA SOMENTE QUANDO FOR SALVO UM USUARIO NOVO POR CAUSA DO # noqa
    # QUE FOI CONFIGURADO EM signals.py e apps.py # noqa
