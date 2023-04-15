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

        # API JSON:
        path("api/v1/", ApiHomeView.as_view(), name="home_api"),
        path("search/api/v1/", ApiSearchView.as_view(), name="search_api"),
        path("tag/api/v1/<slug:slug>", ApiTagView.as_view(), name="tag_api"),
        path("category/api/v1/<int:idcategoria>/", ApiCategoryView.as_view(), name="categoria_api"),
        path("remedios/api/v1/<int:pk>/", ApiRemedioView.as_view(), name="remedio_api"),

        # API REST_FRAMEWORK
        path("api/v2/", Remedios_List_APIv2.as_view(), name="home_rest"),
        path("search/api/v2/", Search_APIv2.as_view(), name="search_rest"),
        path("tag/api/v2/<slug:slug>", Tag_list_APIv2.as_view(), name="tag_rest"),
        path("remedios/api/v2/<int:pk>/", Remedios_Detail_APIv2.as_view(), name="remedio_rest"),
        path("category/api/v2/<int:idcategoria>/", Category_View_APIv2.as_view(), name="categoria_rest"),

    ]
    print('CLASS MODE')
else:
    urlpatterns = [

        path("", home, name="home"),  # HOME == INDEX
        path("search/", search, name="search"),
        path("tag/<slug:slug>", tag, name="tag"),
        path("remedios/<int:pk>/", remedios, name="remedio"),
        path("category/<int:idcategoria>/", categoria, name="categoria"),

        # API REST FRAMEWORK
        path("api/v2/", remedios_api_list, name="home_rest"),
        path("search/api/v2/", search_api_list, name="search_rest"),
        path("tag/api/v2/<slug:slug>", tag_api_list, name="tag_rest"),
        path("remedios/api/v2/<int:pk>/", remedios_api_detail, name="remedio_rest"),
        path("category/api/v2/<int:idcategoria>/", category_api_list, name="categoria_rest"),

        path("theory/", theory, name='theory')  # not important, just tests personals
    ]
    print('FUNC MODE')

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
