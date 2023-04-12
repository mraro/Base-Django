from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from farmacia.models import Remedios
from authors.serializers import Remedio_Serializer


@api_view()
def remedios_api_list(request):
    remedios = Remedios.objects.get_published()
    serializer = Remedio_Serializer(instance=remedios,
                                    many=True,
                                    context={'request': request}
                                    )  # many objects?
    return Response(serializer.data)


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
def tag_api_list(request, slug):
    remedios = Remedios.objects.get_published().filter(tags__slug=slug).order_by('-id')
    serializer = Remedio_Serializer(instance=remedios,
                                    many=True,
                                    context={'request': request}

                                    )  # many objects?
    return Response(serializer.data)
