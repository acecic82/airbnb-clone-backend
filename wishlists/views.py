from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.status import HTTP_200_OK

from rooms.models import Room
from wishlists.models import WishList
from wishlists.serializers import WishlistSerializer

# Create your views here.


class Wishlists(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlists = WishList.objects.filter(user=request.user)
        serializer = WishlistSerializer(
            wishlists,
            many=True,
            context={"request": request},
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = WishlistSerializer(
            data=request.data,
        )

        if serializer.is_valid():
            wishlist = serializer.save(
                user=request.user,
            )
            return Response(
                WishlistSerializer(wishlist).data,
            )
        else:
            raise ParseError


class WishlistDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, user, pk):
        try:
            return WishList.objects.get(pk=pk, user=user)
        except WishList.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        wishlist = self.get_object(request.user, pk)
        serializer = WishlistSerializer(
            wishlist,
            context={
                "request": request,
            },
        )

        return Response(serializer.data)

    def delete(self, request, pk):
        wishlist = self.get_object(request.user, pk)

        wishlist.delete()
        return Response(status=HTTP_200_OK)

    def put(self, request, pk):
        wishlist = self.get_object(request.user, pk)
        serializer = WishlistSerializer(
            wishlist,
            data=request.data,
            partial=True,
            context={
                "request": request,
            },
        )

        if serializer.is_valid():
            wishlist = serializer.save()
            return Response(
                WishlistSerializer(wishlist).data,
            )
        else:
            raise ParseError


class WishlistToggle(APIView):

    def get_wishlist(self, pk):
        try:
            return WishList.objects.get(pk=pk)
        except WishList.DoesNotExist:
            raise NotFound

    def get_room(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def put(self, request, pk, room_pk):
        wishlist = self.get_wishlist(pk)
        room = self.get_room(room_pk)

        # wishlist.rooms.filter(pk=room.pk).exists()
        if wishlist.rooms.contains(room):
            wishlist.rooms.remove(room)
        else:
            wishlist.rooms.add(room)

        return Response(status=HTTP_200_OK)
