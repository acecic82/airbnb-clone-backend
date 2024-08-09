from django.http import HttpResponse
from django.shortcuts import render
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotFound,
    NotAuthenticated,
    ParseError,
    PermissionDenied,
)
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from config import settings
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer
from rooms.models import Amenity, Room
from categories.models import Category
from rooms.serializers import AmenitySerializer, RoomListSerializer, RoomSerializer

# Create your views here.


def SaveRoomWIthOwnerAndCategoryAndAmenity(request, serializer, category_pk):
    if "category" in request.data:
        try:
            category = Category.objects.get(pk=category_pk)
            if category.kind != Category.CategoryKindChoices.ROOMS:
                raise ParseError("The category kind should be 'rooms.'")
        except Category.DoesNotExist:
            raise ParseError("Category not found.")

    try:
        with transaction.atomic():
            if "category" in request.data:
                room = serializer.save(
                    owner=request.user,
                    category=category,
                )
            else:
                room = serializer.save()

            if "amenities" in request.data:
                amenities = request.data.get("amenities")

                room.amenities.clear()
                for amenity_pk in amenities:
                    amenity = Amenity.objects.get(pk=amenity_pk)
                    room.amenities.add(amenity)

            return Response(
                RoomSerializer(room).data,
            )
    except Exception:
        raise ParseError("Amenity not found")


class Rooms(APIView):
    def get(self, request):
        all_rooms = Room.objects.all()
        roomListSerializer = RoomListSerializer(
            all_rooms,
            many=True,
            context={
                "request": request,
            },
        )

        return Response(roomListSerializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            raise NotAuthenticated

        if request.user.is_authenticated:
            serializer = RoomSerializer(
                data=request.data,
            )
            if serializer.is_valid():
                category_pk = request.data.get("category")
                if not category_pk:
                    raise ParseError("Category is required.")
                return SaveRoomWIthOwnerAndCategoryAndAmenity(
                    request, serializer, category_pk
                )
            else:
                return Response(serializer.errors)
        else:
            raise NotAuthenticated


class RoomDeatil(APIView):
    def get_object(self, room_id):
        try:
            return Room.objects.get(pk=room_id)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, room_id):
        room = self.get_object(room_id)
        roomSerializer = RoomSerializer(room)

        return Response(roomSerializer.data)

    def put(self, request, room_id):
        room = self.get_object(room_id)

        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied

        roomSerializer = RoomSerializer(
            room,
            request.data,
            partial=True,
        )

        if roomSerializer.is_valid():
            return SaveRoomWIthOwnerAndCategoryAndAmenity(
                request,
                roomSerializer,
                request.data.get("category"),
            )
        else:
            return Response(roomSerializer.errors)

    def delete(self, request, room_id):
        room = self.get_object(room_id)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if room.owner != request.user:
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)


def see_all_room(request):
    rooms = Room.objects.all()
    return render(
        request,
        "all_rooms.html",
        {
            "rooms": rooms,
            "title": "Hello! this title comes from django!",
        },
    )


def see_one_room(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
        return render(
            request,
            "room_detail.html",
            {
                "room": room,
            },
        )
    except Room.DoesNotExist:
        return render(
            request,
            "room_detail.html",
            {
                "not_found": True,
            },
        )


class Amenities(APIView):
    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(
                AmenitySerializer(amenity).data,
            )
        else:
            return Response(serializer.errors)


class AmenityDeatil(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, amenity_id):
        amenity = self.get_object(amenity_id)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, amenity_id):
        amenity = self.get_object(amenity_id)
        serializer = AmenitySerializer(
            amenity,
            request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(
                AmenitySerializer(updated_amenity).data,
            )
        else:
            return Response(serializer.errors)

    def delete(self, request, amenity_id):
        amenity = self.get_object(amenity_id)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, room_id):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        start = (page - 1) * settings.PAGE_SIZE
        end = page * settings.PAGE_SIZE

        room = self.get_object(room_id)

        reviewSerializer = ReviewSerializer(
            room.reviews.all()[start:end],
            many=True,
        )

        return Response(
            reviewSerializer.data,
        )

    def post(self, request, room_id):
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid():
            review = serializer.save(
                user=request.user,
                room=self.get_object(room_id),
            )

            return Response(ReviewSerializer(review).data)
        else:
            raise ParseError


class RoomAmenities(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, room_id):
        try:
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError:
            page = 1

        room = self.get_object(room_id)

        start = (page - 1) * settings.PAGE_SIZE
        end = page * settings.PAGE_SIZE

        amenitySerializer = AmenitySerializer(
            room.amenities.all()[start:end],
            many=True,
        )

        return Response(amenitySerializer.data)


class RoomPhotos(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, room_id):
        room = self.get_object(room_id)

        if not request.user.is_authenticated:
            raise NotAuthenticated

        if request.user != room.owner:
            raise PermissionDenied

        serializer = PhotoSerializer(data=request.data)

        if serializer.is_valid():
            photo = serializer.save(
                room=room,
            )
            return Response(
                PhotoSerializer(photo).data,
            )

        else:
            raise Response(serializer.errors)
