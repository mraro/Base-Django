from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from authors.serializers import Register_User_Serializer, Login_User_Serializer


class User_Register_Api_v2(CreateAPIView):
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = Register_User_Serializer(data=request.data, context={'request': request}, )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        # serializer.is_valid(raise_exception=True)
        # print("VALIDO")
        # serializer.save(
        #     author=author, is_published=False
        # )

        return Response(request.data, status=201)


class User_Login_Api_v2(ReadOnlyModelViewSet):
    serializer_class = Login_User_Serializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        user = get_user_model()
        qs = user.objects.filter(username=self.request.user.username)
        return qs

    @action(methods=['get', ], detail=False, name='me')
    def me(self, request, *args, **kwargs):  # if don't pass all parameters it will be error
        obj = self.get_queryset().first()
        serializer = self.get_serializer(instance=obj)
        return Response(serializer.data)
