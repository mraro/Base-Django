import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from farmacia.models import Remedios, Category
from farmacia.serializers import Remedio_Serializer
from utility.paginator import make_pagination

"""
APIView - A classe de visualização base que permite criar endpoints personalizados para APIs RESTful.
GenericAPIView - Uma classe de visualização base que fornece métodos auxiliares para processar solicitações HTTP.
ListAPIView - Uma classe de visualização base que retorna uma lista de objetos.
CreateAPIView - Uma classe de visualização base que fornece métodos para criar objetos.
RetrieveAPIView - Uma classe de visualização base que recupera um objeto específico.
UpdateAPIView - Uma classe de visualização base que fornece métodos para atualizar objetos.
DestroyAPIView - Uma classe de visualização base que fornece métodos para excluir objetos.
ListCreateAPIView - Uma classe de visualização base que fornece métodos para listar e criar objetos.
RetrieveUpdateAPIView - Uma classe de visualização base que fornece métodos para recuperar e atualizar objetos.
RetrieveDestroyAPIView - Uma classe de visualização base que fornece métodos para recuperar e excluir objetos.
RetrieveUpdateDestroyAPIView - Uma classe de visualização base que fornece métodos para recuperar, atualizar e excluir objetos.
ReadOnlyAPIView - Uma classe de visualização base que permite apenas leitura, sem permitir que objetos sejam criados, atualizados ou excluídos.
ModelViewSet - Uma classe de visualização base que combina as funcionalidades das visualizações de lista, detalhe, criar, atualizar e excluir em uma única classe.
""" # noqa

# constant (means that not be modified, but you can in .env file) its a var global too.
RANGE_PER_PAGE = int(os.environ.get("RANGE_PER_PAGE", 6))
OBJ_PER_PAGE = int(os.environ.get("OBJ_PER_PAGE", 9))


class OurPagination(PageNumberPagination, LimitOffsetPagination):
    """ in doc, I should use LimitOffsetPagination in settings.py"""
    page_size = 10
    default_limit = 10


class Remedios_List_APIv2(ListAPIView):
    queryset = Remedios.objects.get_published()
    serializer_class = Remedio_Serializer
    pagination_class = OurPagination
    # def get(self, request):
    #     remedios = Remedios.objects.get_published()
    #     serializer = Remedio_Serializer(instance=remedios,
    #                                     many=True,
    #                                     context={'request': request}
    #                                     )  # many objects?
    #     return Response(serializer.data)
    #


class Search_APIv2(APIView):

    @staticmethod
    def get(request):
        var_site = request.GET.get("q")
        if not var_site:
            raise Http404
        else:
            var_site = var_site.strip()  # # '''o | juntamente a função Q faz com que a pesquisa seja OR '''
            medicine = Remedios.objects.filter(Q(title__contains=var_site) |
                                               Q(description__contains=var_site) |
                                               Q(category__name__contains=var_site)).order_by('-id')
            medicine = medicine.filter(is_published=True)
            medicine = medicine.select_related('author', 'category')

        pages = make_pagination(request, medicine, RANGE_PER_PAGE)

        serializer = Remedio_Serializer(instance=medicine,
                                        many=True,
                                        context={'request': request,
                                                 'pages': pages,  # TODO
                                                 'search_done': var_site,
                                                 }
                                        )  # many objects?

        return Response(serializer.data)


class Tag_list_APIv2(APIView):
    def get(self, request, slug):
        var_site = slug
        remedios = Remedios.objects.get_published().filter(tags__slug=var_site).order_by('-id')
        remedios = remedios.select_related("author", "category")
        pages = make_pagination(request, remedios, RANGE_PER_PAGE, OBJ_PER_PAGE)
        serializer = Remedio_Serializer(instance=remedios,
                                        many=True,
                                        context={'request': request,
                                                 'pages': pages,  # TODO
                                                 'search_done': var_site,
                                                 }
                                        )  # many objects?

        return Response(serializer.data)
        # return render(request, "pages/tag.html", context={
        #     'remedios': pages['medicines_page'],
        #     'pages': pages,
        # })


class Remedios_Detail_APIv2(APIView):
    def get(self, request, pk):
        medicine = Remedios.objects.filter(pk=pk).first()

        # medicine = get_object_or_404(medicine)
        serializer = Remedio_Serializer(instance=medicine,
                                        many=False,
                                        context={'request': request,
                                                 }
                                        )  # many objects?

        return Response(serializer.data)


class Category_View_APIv2(APIView):
    def get(self, request, idcategoria):
        medicine = get_list_or_404(
            Remedios.objects.filter(category__id=idcategoria).order_by('-id').select_related('author', 'category')
        )

        serializer = Remedio_Serializer(instance=medicine,
                                        many=True,
                                        context={'request': request,
                                                 }
                                        )  # many objects?

        return Response(serializer.data)