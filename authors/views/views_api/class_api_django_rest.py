from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from authors.models import User
from farmacia import serializers
from farmacia.models import Remedios
from farmacia.views import OurPagination


class Full_CRUD_API_v2(ModelViewSet):
    """
    on urls.py we have to put mode request in as_view({dict}) ex: {'mode':'do'} {'get':'list'}
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet
    """
    queryset = Remedios.objects.all()  # if it has some parameter send by request he will use
    serializer_class = serializers.Dashboard_Serializer
    pagination_class = OurPagination

    def get_queryset(self):
        qs = super().get_queryset()
        print("SUPER IMPORTANT", self.kwargs)  # this comes if it has a pk or slug in link like home/10
        print("SUPER IMPORTANT", self.request.query_params)  # this returns if it has some variable get like \?var=1

        return qs

    @staticmethod
    def list(request):  # NOT USE GET (OR ANY METHOD HTTP), OVERWRITE WHAT HE DOES IN THIS CLASS
        print(request.user)
        remedios = Remedios.objects.filter(is_published=False, author=request.user)
        serializer = serializers.Dashboard_Serializer(instance=remedios,
                                                      context={'request': request},
                                                      many=True
                                                      )
        return Response(serializer.data)

    @staticmethod
    def post(request):  # NOT USE POST (OR ANY METHOD HTTP)
        author = User.objects.get(username=request.user)
        if request.method == "POST":
            serializer = serializers.Dashboard_Serializer(data=request.data, context={'request': request}, )
            # serializer.is_published = False
            # serializer.author = author
            serializer.is_valid(raise_exception=True)
            print("VALIDO")
            serializer.save(
                author=author, is_published=False
            )
            # messages.success(request, "Medicine Created and send to analise")
            return Response(serializer.data, status=201)


"""
class Api_Dashboard_v2(APIView):
    @staticmethod
    def get(request):
        print(request.user)
        remedios = Remedios.objects.filter(is_published=False, author=request.user)
        serializer = serializers.Dashboard_Serializer(instance=remedios,
                                                      context={'request': request},
                                                      many=True
                                                      )
        return Response(serializer.data)

    @staticmethod
    def post(request):
        author = User.objects.get(username=request.user)
        if request.method == "POST":
            serializer = serializers.Dashboard_Serializer(data=request.data, context={'request': request}, )
            # serializer.is_published = False
            # serializer.author = author
            serializer.is_valid(raise_exception=True)
            print("VALIDO")
            serializer.save(
                author=author, is_published=False
            )
            # messages.success(request, "Medicine Created and send to analise")
            return Response(serializer.data, status=201)


class Api_CRUD_v2(RetrieveUpdateDestroyAPIView):
    queryset = Remedios.objects.all()
    serializer_class = serializers.Dashboard_Serializer
    pagination_class = OurPagination
"""
