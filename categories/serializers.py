from rest_framework import serializers

from rooms.models import Amenity
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "kind",
        )
