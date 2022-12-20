from django.urls import path

from recipes.views import *




urlpatterns = [

    path("", home),  # HOME == INDEX
    path("sobre/", sobre),
    path("contato/", contato),
]
