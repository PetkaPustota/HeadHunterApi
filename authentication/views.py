from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import UserCreateSerializer


# Create your views here.
class UserCreateView(CreateAPIView):
    model = User
    serializer_class = UserCreateSerializer


class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

