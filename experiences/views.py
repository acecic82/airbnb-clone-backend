from datetime import datetime
from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import ParseError

from bookings.models import Booking
from bookings.serializers import (
    CreateExperienceBookingSerializer,
    PublicBookingSerializer,
)
from categories.models import Category
from experiences.models import Experience, Perk
from experiences.serializers import (
    ExperienceDetailSerializer,
    ExperienceSerializer,
    PerkSerializer,
    TinyPerkSerializer,
)

# Create your views here.


class Perks(APIView):
    def get(self, request):
        perks = Perk.objects.all()

        perkSerializer = PerkSerializer(
            perks,
            many=True,
        )
        return Response(
            perkSerializer.data,
        )

    def post(self, request):
        perkSerializer = PerkSerializer(
            data=request.data,
        )
        if perkSerializer.is_valid():
            perk = perkSerializer.save()
            return Response(
                PerkSerializer(perk).data,
            )
        else:
            return Response(perkSerializer.errors)


class PerkDetail(APIView):
    def get_object(self, perk_id):
        try:
            return Perk.objects.get(pk=perk_id)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, perk_id):
        perk = self.get_object(perk_id)
        return Response(
            PerkSerializer(perk).data,
        )

    def put(self, request, perk_id):
        perk = self.get_object(perk_id)
        perkSerializer = PerkSerializer(
            perk,
            data=request.data,
            partial=True,
        )

        if perkSerializer.is_valid():
            updated_perk = perkSerializer.save()
            return Response(
                PerkSerializer(updated_perk).data,
            )
        else:
            return Response(perkSerializer.errors)

    def delete(self, request, perk_id):
        perk = self.get_object(perk_id)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class ExperiencePerks(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, experience_pk):
        try:
            experience = Experience.objects.get(pk=experience_pk)
        except Experience.DoesNotExist:
            raise NotFound
        perks = []

        for perk in experience.perks.all():
            perks.append(perk)

        serializer = TinyPerkSerializer(
            experience.perks,
            many=True,
        )

        return Response(serializer.data)


def checkValidAndGetCategory(category_pk):
    print(category_pk)
    try:
        category = Category.objects.get(pk=category_pk)
        if category.kind != Category.CategoryKindChoices.EXPERIENCE:
            raise ParseError("Category kind should be Experience")
    except Category.DoesNotExist:
        raise ParseError("Category can not found")

    return category


def checkValidAndGetPerk(perk_pk):
    try:
        perk = Perk.objects.get(pk=perk_pk)
    except Perk.DoesNotExist:
        raise ParseError("Perk can not found")

    return perk


class Experiences(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        experiences = Experience.objects.all()

        serializer = ExperienceSerializer(
            experiences,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = ExperienceSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    category_pk = request.data.get("category")

                    category = checkValidAndGetCategory(category_pk)

                    perk_pks = request.data.get("perks")

                    perks = []

                    for perk_pk in perk_pks:
                        perk = checkValidAndGetPerk(perk_pk)
                        perks.append(perk)

                    experience = serializer.save(
                        host=request.user,
                        category=category,
                        perks=perks,
                    )

                    return Response(
                        ExperienceSerializer(experience).data,
                    )

            except Exception:
                raise ParseError("Fail to create Experience")

        else:
            return Response(serializer.errors)


class ExperienceDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, experience_pk):
        experience = self.get_object(experience_pk)

        serializer = ExperienceDetailSerializer(experience)
        return Response(serializer.data)

    def put(self, request, experience_pk):
        experience = self.get_object(experience_pk)

        serializer = ExperienceSerializer(
            experience,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    if "category" in request.data:
                        category_pk = request.data.get("category")
                        category = checkValidAndGetCategory(category_pk)

                    if "perks" in request.data:
                        perk_pks = request.data.get("perks")
                        experience.perks.clear()

                        for perk_pk in perk_pks:
                            perk = checkValidAndGetPerk(perk_pk)
                            experience.perks.add(perk)

                    experience = serializer.save(
                        host=request.user,
                        category=category if "category" in request.data else None,
                    )

                    return Response(
                        ExperienceSerializer(experience).data,
                    )

            except Exception:
                raise ParseError("Fail to update Experience")
        else:
            Response(serializer.errors)

    def delete(self, request, experience_pk):
        experience = self.get_object(experience_pk)

        experience.delete()

        return Response(status=HTTP_204_NO_CONTENT)


class ExperienceBookings(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, experience_pk):
        experience = self.get_object(experience_pk)

        bookings = Booking.objects.filter(
            experience=experience,
        )

        serializer = PublicBookingSerializer(
            bookings,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request, experience_pk):
        experience = self.get_object(experience_pk)

        serializer = CreateExperienceBookingSerializer(
            data=request.data,
            context={
                "experience": experience,
                "experience_time": request.data.get("experience_time"),
            },
        )

        if serializer.is_valid():

            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
                experience_time=request.data.get("experience_time"),
            )

            serializer = PublicBookingSerializer(booking)

            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class ExperienceBookingDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, experience_pk, booking_pk):
        try:
            Experience.objects.get(pk=experience_pk)
            return Booking.objects.get(pk=booking_pk)
        except Experience.DoesNotExist:
            raise NotFound("Experience not found")
        except Booking.DoesNotExist:
            raise NotFound("Booking not found")

    def get(self, request, experience_pk, booking_pk):
        booking = self.get_object(experience_pk, booking_pk)

        serializer = PublicBookingSerializer(
            booking,
        )

        return Response(serializer.data)

    def put(self, request, experience_pk, booking_pk):
        booking = self.get_object(experience_pk, booking_pk)

        if "experience_time" in request.data:

            now = timezone.localtime(timezone.now())
            experience_time = request.data.get("experience_time")
            experience_time = datetime.strptime(experience_time, "%Y-%m-%dT%H:%M:%S%z")

            if now > experience_time:
                raise ParseError("Can't modify in the past!")

        serializer = PublicBookingSerializer(
            booking,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            updated_booking = serializer.save()

            serializer = PublicBookingSerializer(
                updated_booking,
            )

            return Response(serializer.data)

        else:
            return Response(serializer.errors)

    def delete(self, request, experience_pk, booking_pk):
        booking = self.get_object(experience_pk, booking_pk)

        booking.delete()

        return Response(status=HTTP_204_NO_CONTENT)
