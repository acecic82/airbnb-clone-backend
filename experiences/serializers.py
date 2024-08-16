from rest_framework import serializers
from .models import Experience, Perk


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"

    def validate(self, data):
        if data["start"] >= data["end"]:
            raise serializers.ValidationError("start should be smaller than end.")


class PerkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"
