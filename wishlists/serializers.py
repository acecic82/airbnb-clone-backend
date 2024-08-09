from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer

from rooms.serializers import RoomListSerializer, RoomSerializer
from wishlists.models import WishList


class WishlistSerializer(ModelSerializer):

    rooms = RoomListSerializer(many=True, read_only=True)

    class Meta:
        model = WishList
        fields = (
            "name",
            "rooms",
        )
