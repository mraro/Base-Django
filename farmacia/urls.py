from farmacia.views import *
from django.urls import path

## PAGINA ADICIONADA MANUALMENTE QUE GERENCIA OS LINKS

app_name = "farmacia"

urlpatterns = [

    path("", home, name="home"),  # HOME == INDEX
    path("cadastro/", cadastro, name="cadastro"),
    path("remedios/<int:idremedios>/", remedios, name="remedio"),
]
