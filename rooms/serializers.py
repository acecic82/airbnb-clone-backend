from rest_framework import serializers

from categories.serializers import CategorySerializer
from medias.serializers import PhotoSerializer
from reviews.serializers import ReviewSerializer
from rooms.models import Amenity, Room
from users.serializers import TinyUserSerializer


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )


class RoomListSerializer(serializers.ModelSerializer):
    # # get_xxx 형태의 def 를 호출함
    # rating = serializers.SerializerMethodField()

    # # rating 을 선언하면 이걸 호출(SerializerMethodField())
    # def get_rating(self, room):
    #     return room.rating()

    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(many=True, read_only=True)

    def get_is_owner(self, room):
        request = self.context["request"]
        return request.user == room.owner

    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )


class RoomSerializer(serializers.ModelSerializer):

    owner = TinyUserSerializer(
        read_only=True,
    )
    amenities = AmenitySerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    # reviews = ReviewSerializer(
    #     many=True,
    #     read_only=True,
    # )

    photos = PhotoSerializer(
        many=True,
        read_only=True,
    )

    # get_xxx 형태의 def 를 호출함
    rating = serializers.SerializerMethodField()

    # rating 을 선언하면 이걸 호출(SerializerMethodField())
    def get_rating(self, room):
        return room.rating()

    class Meta:
        model = Room
        fields = "__all__"
