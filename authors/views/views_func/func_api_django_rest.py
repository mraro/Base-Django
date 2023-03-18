from farmacia import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from farmacia import models


@api_view()
def api_create_obj(request):

    return Response()


@api_view()
def api_dashboard(request):
    remedios = models.Remedios.objects.filter(is_published=False, author=request.user)
    serializer = serializers.Remedio_Serializer(instance=remedios,
                                                context={'request': request},
                                                many=True
                                                )
    return Response(serializer.data)


@api_view()
def api_edit_obj(request, pk):
    return Response()


@api_view()
def api_delete_obj(request, pk):
    return Response()
