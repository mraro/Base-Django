from farmacia.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from authors.views import *

# PAGINA ADICIONADA MANUALMENTE QUE GERENCIA OS LINKS   # noqa

app_name = "authors"
METHOD_MODE = int(os.environ.get("METHOD_MODE", 1))
if METHOD_MODE == 0:
    urlpatterns = [
        # view, since path waits for func we use as_view() to use a classe as func here
        # this is a class base
        path("", HomeView.as_view(), name="home"),  # HOME == INDEX

        path("register/", Register_View.as_view(), name="register"),
        path("register/create/", Register_Create.as_view(), name="register_create"),
        path("login", Login_View.as_view(), name="login"),
        path("login/authenticate/", Login_Authenticate.as_view(), name="authenticate"),
        path("logout/", Logout_Backend.as_view(), name="logout"),

        path("dashboard/", DashboardView.as_view(), name="dashboard"),  # R     read
        path("dashboard/create/", BaseObjectClassedView.as_view(), name="create"),  # create
        path("dashboard/<int:idobject>/edit/", BaseObjectClassedView.as_view(), name="edit"),
        path("dashboard/<int:idobject>/delete/", ObjectClassedViewDelete.as_view(), name="delete"),  # D     delete
    ]

else:
    urlpatterns = [
        path("", home, name="home"),  # HOME == INDEX

        path("register/", register_view, name="register"),
        path("register/create/", register_create, name="register_create"),
        path("login", login_view, name="login"),
        path("login/authenticate/", login_authenticate, name="authenticate"),
        path("logout/", logout_backend, name="logout"),

        path("dashboard/create/", create_obj, name="create"),                   # C     create
        path("dashboard/", dashboard, name="dashboard"),                        # R     read
        path("dashboard/<int:idobject>/edit/", edit_obj, name="edit"),          # U     update
        path("dashboard/<int:idobject>/delete/", delete_obj, name="delete"),    # D     delete
    ]

# CUIDADO PARA NÃO REPETIR O NOME OU QLQR OUTRA COISA

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
