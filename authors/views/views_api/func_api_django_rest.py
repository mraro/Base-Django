from django.shortcuts import get_object_or_404

from farmacia import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from farmacia import models


@api_view(['GET', ])  # GET is read
def api_dashboard(request):
    remedios = models.Remedios.objects.filter(is_published=False, author=request.user)
    serializer = serializers.Dashboard_Serializer(instance=remedios,
                                                  context={'request': request},
                                                  many=True
                                                  )
    return Response(serializer.data)


@api_view(http_method_names=["PATCH", ])    # PATCH is update
def api_edit_obj(request, pk):
    remedio = models.Remedios.objects.filter(pk=pk, is_published=False, author=request.user).first()

    author = models.User.objects.get(username=request.user)
    if request.method == "PATCH":
        serializer = serializers.Dashboard_Serializer(data=request.data,
                                                      context={'request': request},
                                                      instance=remedio,
                                                      partial=True)  # partial means that part of data might be changed
        serializer.is_published = False
        serializer.author = author
        serializer.is_valid(raise_exception=True)
        print("VALIDO")
        serializer.save()
        # messages.success(request, "Medicine Created and send to analise")
        return Response(serializer.data, status=201)

    return Response(status=418)


@api_view(http_method_names=["POST", ])     # POST is create
def api_create_obj(request):
    author = models.User.objects.get(username=request.user)
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
        # return Response(serializer.data, status=201)


@api_view(http_method_names=["DELETE", ])      # DELETE is DELETE kk
def api_delete_obj(request, pk):
    remedio = models.Remedios.objects.filter(pk=pk, is_published=False, author=request.user).first()
    if remedio is None:
        return Response(status=404)
    if request.method == "DELETE":
        remedio.delete()
        return Response(status=204)
