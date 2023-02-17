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
    path("register/create/", register_create, name="register_create"),
    path("login", login_view, name="login"),
    path("login/authenticate", login_authenticate, name="authenticate"),
    path("logout/", logout_backend, name="logout"),
    path("dashboard/create/", create_obj, name="create"),                 # C     create
    path("dashboard/", dashboard, name="dashboard"),                      # R     read
    path("dashboard/<int:idobject>/edit/", edit_obj, name="edit"),        # U     update
    path("dashboard/<int:idobject>/delete/", delete_obj, name="delete"),  # D     delete
]
# CUIDADO PARA NÃO REPETIR O NOME OU QLQR OUTRA COISA

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
