from django.shortcuts import redirect
from rest_framework.reverse import reverse

from farmacia import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from farmacia import models


@api_view()
def api_dashboard(request):
    remedios = models.Remedios.objects.filter(is_published=False, author=request.user)
    serializer = serializers.Dashboard_Serializer(instance=remedios,
                                                  context={'request': request},
                                                  many=True
                                                  )
    return Response(serializer.data)


@api_view()
def api_edit_obj(request, pk):
    remedio = models.Remedios.objects.filter(pk=pk, is_published=False, author=request.user).first()
    serializer = serializers.Dashboard_Serializer(instance=remedio,
                                                  context={'request': request},
                                                  many=False
                                                  )
    # form = EditObjectForm(
    #     data=request.POST or None,  # receive a request data or none
    #     files=request.FILES or None,
    #     instance=remedio[0]  # if none receive what will be edited
    # )
    # if form.is_valid():
    #     object_data = form.save(commit=False)
    #     # print(type(object_data.author))

    # object_data.is_published = False
    # object_data.save()

    # messages.success(request, _("Medicine Saved"))
    # return redirect(reverse('authors:dashboard'))
    return Response(serializer.data)


@api_view(http_method_names=["POST", ])
def api_create_obj(request):
    author = models.User.objects.get(username=request.user)
    if request.method == "POST":
        serializer = serializers.Dashboard_Serializer(data=request.data, context={'request': request}, )
        # form = EditObjectForm(
        #     data=request.POST or None,
        #     files=request.FILES or None,
        # )
        print(serializer)
        serializer.is_valid(raise_exception=True)
        # serializer.is_published = False
        # object_data.author = author
        print("VALIDO")
        # serializer.save()
        # messages.success(request, "Medicine Created and send to analise")
        return Response(serializer.data, status=201)
        # return Response(serializer.data, status=201)

        # return redirect(reverse('authors:create_rest'))


@api_view()
def api_delete_obj(request, pk):
    return Response()
