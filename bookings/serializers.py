import datetime
from django.utils import timezone
from rest_framework import serializers
from .models import Booking


class CreateRoomBookingSerializer(serializers.ModelSerializer):

    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            "check_in",
            "check_out",
            "guests",
        )

    def validate_check_in(self, value):
        now = timezone.localtime(timezone.now()).date()

        if now > value:
            raise serializers.ValidationError("Can't book in the past!")

        return value

    def validate_check_out(self, value):
        now = timezone.localtime(timezone.now()).date()

        if now > value:
            raise serializers.ValidationError("Can't book in the past!")

        return value

    def validate(self, data):
        if data["check_out"] <= data["check_in"]:
            raise serializers.ValidationError(
                "Check in should be smaller than check out."
            )
        room = self.context.get("room")

        if Booking.objects.filter(
            room=room,
            check_in__lte=data["check_out"],
            check_out__gte=data["check_in"],
        ).exists():
            raise serializers.ValidationError(
                "Those (or some) of those dates are already taken."
            )
        return data


class CreateExperienceBookingSerializer(serializers.ModelSerializer):

    experience_time = serializers.DateTimeField()

    class Meta:
        model = Booking
        fields = (
            "experience_time",
            "guests",
        )

    def validate_experience_time(self, value):
        now = timezone.localtime(timezone.now()).date()
        date = value.date()

        if now > date:
            raise serializers.ValidationError("Can't book in the past!")

        return value

    def validate(self, data):
        experience = self.context.get("experience")

        experience_date = self.context.get("experience_time")
        experience_date_time = datetime.datetime.strptime(
            experience_date, "%Y-%m-%dT%H:%M:%S%z"
        )

        bookings = Booking.objects.filter(
            experience=experience,
            experience_time__gte=experience_date_time,
        )

        for booking in bookings.all():
            booking_date = booking.experience_time.date()

            if booking_date == experience_date_time.date():
                raise serializers.ValidationError("Alread booked this time")

        return data


class PublicBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )
