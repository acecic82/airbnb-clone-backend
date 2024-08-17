from rest_framework import serializers

from categories.serializers import CategorySerializer
from users.serializers import TinyUserSerializer
from .models import Experience, Perk


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"

    def validate(self, data):
        if "start" in data and "end" in data and data["start"] >= data["end"]:
            raise serializers.ValidationError("start should be smaller than end.")
        return data


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"


class TinyPerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = (
            "name",
            "details",
            "explanation",
        )


class ExperienceDetailSerializer(serializers.ModelSerializer):
    host = TinyUserSerializer(
        read_only=True,
    )
    perks = TinyPerkSerializer(
        read_only=True,
        many=True,
    )
    category = CategorySerializer(
        read_only=True,
    )

    class Meta:
        model = Experience
        fields = "__all__"
