from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from . import serializers

# Create your views here.


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)

        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            savedUser = serializer.save()
            return Response(serializers.PrivateUserSerializer(savedUser).data)
        else:
            return Response(serializer.errors)


class Users(APIView):
    def post(self, request):
        serializer = serializers.PrivateUserSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            pass
        else:
            return Response(serializer.errors)
