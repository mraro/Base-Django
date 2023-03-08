import os

from django.db.models import Q, Value, F
from django.db.models.functions import Concat
from django.shortcuts import get_list_or_404, Http404  # object é para um só elemento
from django.views.generic import ListView, DetailView

from farmacia.models import Remedios, Category

from utility.paginator import make_pagination

# constant (means that not be modified, but you can in .env file) it's a var global too.
RANGE_PER_PAGE = int(os.environ.get("RANGE_PER_PAGE", 6))
OBJ_PER_PAGE = int(os.environ.get("OBJ_PER_PAGE", 9))


# THIS MAKES THE SAME THING OF func home {
class ObjectListViewBase(ListView):
    # This is what I can overwrite
    # allow_empty = True
    # queryset = None
    model = Remedios  # DATABASE
    # paginate_by = None
    # paginate_orphans = 0
    context_object_name = 'remedios'  # TABLE
    # paginator_class = Paginator
    # page_kwarg = "page"
    ordering = ['-id']  # ORDERBY
    template_name = 'pages/home.html'

    def get_queryset(self, *args, **kwargs):  # RETURN A QUERYSET IN THE ORDER WORDS READ DATABASE
        # AQUI O get_published EM MODELS NÃO CHEGA
        querySet = super(ObjectListViewBase, self).get_queryset()
        querySet = querySet.filter(is_published=True, )  # (FILTER),, send data to web template html
        querySet = querySet.annotate(  # GIVE MORE ONE VARIABLE INTO A LIST OF QUERYSET
            author_full_name=Concat(
                F('author__first_name'),
                Value(" "),
                F('author__last_name'),
            )
        )
        querySetLight = querySet.select_related('author', 'category')  # ! THIS IMPROVE DATABASE READ
        # querySetLight = querySet.prefetch_related('author', 'category')   # ! THIS IMPROVES DATABASE READ TOO
        return querySetLight

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        pages = make_pagination(self.request, context.get('remedios'), RANGE_PER_PAGE, OBJ_PER_PAGE)
        category = Category.objects.filter(remedios__isnull=False).distinct()
        context.update(
            {'remedios': pages['medicines_page'],
             'pages': pages,
             'nameSite': 'Farma Class',
             'categories': category,
             }
        )
        return context  # UPDATE CONTEXT, IN THE OTHER WORDS, CUSTOMIZE WEB TEMPLATE WITH MY PAGINATION FUNC


# } END COMMENT

class HomeView(ObjectListViewBase):
    ...


class CategoryView(ObjectListViewBase):
    template_name = 'pages/category-view.html'

    # def get(self, *args, **kwargs):
    #     raise Http404

    def get_queryset(self, *args, **kwargs):  # RETURN A QUERYSET IN THE ORDER WORDS READ DATABASE
        querySet = super(ObjectListViewBase, self).get_queryset()
        querySet = querySet.filter(category__id=self.kwargs.get('idcategoria')).order_by(
            '-id')  # (FILTER) send data to web template html
        querySetLight = querySet.select_related('author', 'category')  # ! THIS IMPROVE DATABASE READ
        get_list_or_404(querySetLight)
        return querySetLight

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryView, self).get_context_data()
        medicines = context.get('remedios')
        pages = make_pagination(self.request, medicines, RANGE_PER_PAGE, OBJ_PER_PAGE)
        context.update(
            {
                # 'remedios': medicine,
                'remedios': pages['medicines_page'],
                'pages': pages,
                'categoryTitle': f'{medicines[0].category.name}',  # ISSO É PY: F'{ VARIAVEL}' RETORNA STRING
                'is_detail': False,
            }
        )
        return context


class SearchView(ObjectListViewBase):
    template_name = 'pages/search.html'

    def get_queryset(self, *args, **kwargs):
        querySet = super(SearchView, self).get_queryset()
        var_site = self.request.GET.get('q')
        if not var_site:
            raise Http404
        var_site = var_site.strip()  # # '''o | juntamente a função Q faz com que a pesquisa seja OR '''
        querySet = querySet.filter(Q(title__contains=var_site) |
                                   Q(description__contains=var_site) |
                                   Q(category__name__contains=var_site)).order_by('-id')
        querySet = querySet.filter(is_published=True)
        querySetLight = querySet.select_related('author', 'category')  # ! THIS IMPROVE DATABASE READ

        return querySetLight

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data()
        var_site = self.request.GET.get('q')
        var_site = var_site.strip()  # # '''o | juntamente a função Q faz com que a pesquisa seja OR '''

        pages = make_pagination(self.request, context.get('remedios'), RANGE_PER_PAGE, OBJ_PER_PAGE)
        context.update(
            {
                'remedios': pages['medicines_page'],
                'pages': pages,
                'search_done': var_site,
            }
        )
        return context


class TagView(ObjectListViewBase):
    template_name = 'pages/tag.html'

    def get_queryset(self, *args, **kwargs):
        querySet = super(TagView, self).get_queryset()
        var_site = self.kwargs.get('slug')

        if not var_site:
            raise Http404
        # var_site = var_site.strip()  # # '''o | juntamente a função Q faz com que a pesquisa seja OR '''
        querySet = querySet.filter(tags__slug=var_site).order_by('-id')
        querySet = querySet.filter(is_published=True)
        querySetLight = querySet.select_related('author', 'category')  # ! THIS IMPROVE DATABASE READ

        return querySetLight

    def get_context_data(self, *args, **kwargs):
        context = super(TagView, self).get_context_data()
        # var_site = self.kwargs.get('slug')

        pages = make_pagination(self.request, context.get('remedios'), RANGE_PER_PAGE, OBJ_PER_PAGE)
        context.update(
            {
                'remedios': pages['medicines_page'],
                'pages': pages,
                # 'title': var_site
            }
        )
        return context


class RemedioView(DetailView):
    # DETAIL VIEW WAITS PK

    model = Remedios
    context_object_name = 'remedio'
    template_name = 'pages/remedio-view.html'

    def get_context_data(self, **kwargs):
        context = super(RemedioView, self).get_context_data()

        context.update({
            'is_detail': True,
        })
        return context
