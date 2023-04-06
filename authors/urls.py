from farmacia.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from authors.views import *

# from rest_framework.routers import SimpleRouter
# PAGINA ADICIONADA MANUALMENTE QUE GERENCIA OS LINKS   # noqa

app_name = "authors"

# farmacia_api_v2_router = SimpleRouter()
# farmacia_api_v2_router.register(
#     'dashboard/api/v2',
#     Full_CRUD_API_v2,
#     basename='rest_',
# )

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

        path("dashboard/create/", BaseObjectClassedView.as_view(), name="create"),              # C     create
        path("dashboard/", DashboardView.as_view(), name="dashboard"),                          # R     read
        path("dashboard/<int:pk>/edit/", BaseObjectClassedView.as_view(), name="edit"),         # U     update
        path("dashboard/<int:pk>/delete/", ObjectClassedViewDelete.as_view(), name="delete"),   # D     delete

        path("dashboard/api/v2/create/", Full_CRUD_API_v2.as_view({'post': 'create'}), name="rest_create_rest"),
        # C     create  (POST)
        path("dashboard/api/v2/", Full_CRUD_API_v2.as_view({'get': 'list'}), name="rest_dashboard"),
        # R     read  (GET)
        path("dashboard/api/v2/<int:pk>/edit/", Full_CRUD_API_v2.as_view({'patch': 'partial_update'}),
             name="rest_edit"),
        # U     update  (PATCH ou put)
        path("dashboard/api/v2/<int:pk>/delete/", Full_CRUD_API_v2.as_view({'delete': 'destroy'}), name="rest_delete"),
        # D     delete   (DELETE)
    ]

else:
    urlpatterns = [
        path("", home, name="home"),  # HOME == INDEX

        path("register/", register_view, name="register"),
        path("register/create/", register_create, name="register_create"),
        path("login", login_view, name="login"),
        path("login/authenticate/", login_authenticate, name="authenticate"),
        path("logout/", logout_backend, name="logout"),

        path("dashboard/create/", create_obj, name="create"),           # C     create
        path("dashboard/", dashboard, name="dashboard"),                # R     read
        path("dashboard/<int:pk>/edit/", edit_obj, name="edit"),        # U     update
        path("dashboard/<int:pk>/delete/", delete_obj, name="delete"),  # D     delete

        path("dashboard/api/v2/create/", api_create_obj, name="create_rest"),           # C     create  (POST)
        path("dashboard/api/v2/", api_dashboard, name="dashboard_rest"),                # R     read  (GET)
        path("dashboard/api/v2/<int:pk>/edit/", api_edit_obj, name="edit_rest"),        # U     update  (PATCH ou put)
        path("dashboard/api/v2/<int:pk>/delete/", api_delete_obj, name="delete_rest"),  # D     delete   (DELETE)
    ]

# CUIDADO PARA NÃO REPETIR O NOME OU QLQR OUTRA COISA # noqa

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
