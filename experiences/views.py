from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from experiences.models import Perk
from experiences.serializers import PerkSerializer

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
