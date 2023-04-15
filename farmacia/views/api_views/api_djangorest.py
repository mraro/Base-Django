from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import OrderedDict
from farmacia.models import Remedios
from authors.serializers import Remedio_Serializer
from utility.paginator import make_pagination
import os

RANGE_PER_PAGE = int(os.environ.get("RANGE_PER_PAGE", 6))
OBJ_PER_PAGE = int(os.environ.get("OBJ_PER_PAGE", 9))


def serializer_with_own_pagination(request, queryset):
    """ extracted to re-use where is a function with pagination (it made to appear with class mode """
    pages = make_pagination(request, queryset, RANGE_PER_PAGE, OBJ_PER_PAGE)

    data = pages['medicines_page']  # < use or paginator
    count = len(queryset)   # < get len of data

    if data.has_previous():
        previous_page = f"/api/v2/?page={data.previous_page_number()}"
    else:
        previous_page = None
    if data.has_next():
        next_page = f"/api/v2/?page={data.next_page_number()}"
    else:
        next_page = None

    serializer = Remedio_Serializer(instance=data,
                                    many=True,
                                    context={'request': request}
                                    )  # many objects?

    serialized_data = serializer.data
    return Response({"count": count,
                     "next": next_page,
                     "previous": previous_page,
                     "results": serialized_data})


@api_view()
def remedios_api_list(request):
    remedios = Remedios.objects.get_published()

    return serializer_with_own_pagination(request, remedios)


@api_view()
def remedios_api_detail(request, pk):
    remedios = get_object_or_404(
        Remedios.objects.get_published(), pk=pk
    )
    serializer = Remedio_Serializer(instance=remedios,
                                    many=False,
                                    context={'request': request}
                                    )  # many objects?
    return Response(serializer.data)


@api_view()
def category_api_list(request, idcategoria):
    medicine = get_list_or_404(
        Remedios.objects.filter(category__id=idcategoria).order_by('-id').select_related('author', 'category')
    )
    return serializer_with_own_pagination(request, medicine)


@api_view()
def search_api_list(request):
    var_site = request.GET.get("q")
    if not var_site:
        raise Http404
    var_site = var_site.strip()  # # '''o | juntamente a função Q faz com que a pesquisa seja OR '''
    medicine = Remedios.objects.filter(Q(title__contains=var_site) |
                                       Q(description__contains=var_site) |
                                       Q(category__name__contains=var_site)).order_by('-id')
    medicine = medicine.filter(is_published=True)

    return serializer_with_own_pagination(request, medicine)



@api_view()
def tag_api_list(request, slug):
    var_site = slug
    remedios = Remedios.objects.get_published().filter(tags__slug=var_site).order_by('-id')
    remedios = remedios.select_related("author", "category")

    return serializer_with_own_pagination(request, remedios)

