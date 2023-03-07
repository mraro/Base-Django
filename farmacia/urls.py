from farmacia.views import *
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

## PAGINA ADICIONADA MANUALMENTE QUE GERENCIA OS LINKS

app_name = "farmacia"
METHOD_MODE = os.environ.get("METHOD_MODE")
if METHOD_MODE == '0':
    urlpatterns = [

        path("", HomeView.as_view(), name="home"),  # HOME == INDEX
        path("search/", SearchView.as_view(), name="search"),
        path("tag/<slug:slug>", TagView.as_view(), name="tag"),
        path("category/<int:idcategoria>/", CategoryView.as_view(), name="categoria"),
        path("remedios/<int:pk>/", RemedioView.as_view(), name="remedio"),

        # API:
        path("api/v1/", ApiHomeView.as_view(), name="home_api"),
        path("remedios/api/v1/<int:pk>/", ApiRemedioView.as_view(), name="remedio_api"),
        # TODO MAIS APIS
    ]
    print('CLASS MODE')
else:
    urlpatterns = [

        path("", home, name="home"),  # HOME == INDEX
        path("search/", search, name="search"),
        path("remedios/<int:idremedios>/", remedios, name="remedio"),
        path("category/<int:idcategoria>/", categoria, name="categoria"),

        path("theory/", theory, name='theory')
    ]
    print('FUNC MODE')

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
