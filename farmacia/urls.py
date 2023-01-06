from farmacia.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

## PAGINA ADICIONADA MANUALMENTE QUE GERENCIA OS LINKS

app_name = "farmacia"

urlpatterns = [

    path("", home, name="home"),  # HOME == INDEX
    path("cadastro/", cadastro, name="cadastro"),
    path("remedios/<int:idremedios>/", remedios, name="remedio"),
    path("category/<int:idcategoria>/", categoria, name="categoria")

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
