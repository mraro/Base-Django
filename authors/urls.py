from farmacia.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from authors.views import *
# PAGINA ADICIONADA MANUALMENTE QUE GERENCIA OS LINKS

app_name = "authors"

urlpatterns = [

    path("", home, name="home"),  # HOME == INDEX
    path("register/", register_view, name="register"),
    path("register/create/", register_create, name="create"),
    path("login", login_view, name="login"),
    path("login_autenticate", login_authenticate, name="authenticate"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
