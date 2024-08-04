from django.shortcuts import render
from categories.models import Category
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .serializers import CategorySerializer

# Create your views here.


class Categories(APIView):
    def get(self, request):
        all_categories = Category.objects.all()
        serializer = CategorySerializer(
            all_categories,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            new_category = serializer.save()
            return Response(
                CategorySerializer(new_category).data,
            )
        else:
            return Response(serializer.errors)


class CategoryDetail(APIView):
    def get_object(self, category_id):
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise NotFound

        return category

    def get(self, request, category_id):
        serializer = CategorySerializer(self.get_object(category_id))
        return Response(serializer.data)

    def put(self, request, category_id):
        serializer = CategorySerializer(
            self.get_object(category_id),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, category_id):
        self.get_object(category_id).delete()
        return Response(status=HTTP_204_NO_CONTENT)
