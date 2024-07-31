from django.contrib import admin
from django.forms import models
from categories.models import Category
from rooms.models import Amenity, Room

# Register your models here.


@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, rooms):
    for room in rooms.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    actions = (reset_prices,)

    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "rating",
        "owner",
        "created_at",
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

    search_fields = (
        # contains
        "name",
        # startwith
        "^price",
        # exact -> =price
        # foreignKey -> User.username contain case
        # you can also use ^owner__username"
        "owner__username",
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
