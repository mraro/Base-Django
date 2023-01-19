from farmacia.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from authors.views import *
# PAGINA ADICIONADA MANUALMENTE QUE GERENCIA OS LINKS

app_name = "authors"

urlpatterns = [

    path("", home, name="home"),  # HOME == INDEX
    path("cadastro/", register_view, name="cadastro"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
