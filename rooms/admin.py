from django.contrib import admin
from django.forms import models
from categories.models import Category
from rooms.models import Amenity, Room

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "price",
        "kind",
        "owner",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "country",
        "city",
        "price",
        "rooms",
        "toilets",
        "pet_friendly",
        "kind",
        "amenities",
        "created_at",
        "updated_at",
    )

    def get_form(self, request, obj=None, **kwargs):
        print(f"In get form")
        form = super(RoomAdmin, self).get_form(request, obj, **kwargs)
        print(f"created form")
        form.base_fields["category"].queryset = Category.objects.filter(kind="rooms")
        return form


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
