from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated
from .models import Photo

# Create your views here.


class PhotoDetail(APIView):

    # IsAuthenticatedOrReadOnly 는 get은 인증 없이도 통과되게 할 수 있다.
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            raise NotFound

    def delete(self, request, pk):
        photo = self.get_object(pk)

        if photo.room:
            if photo.room.owner != request.user:
                raise PermissionDenied
        elif photo.experience:
            if photo.experience.host != request.user:
                raise PermissionDenied

        photo.delete()
        return Response(status=HTTP_200_OK)
