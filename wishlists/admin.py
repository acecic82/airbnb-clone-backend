from django.contrib import admin

from wishlists.models import WishList

# Register your models here.


@admin.register(WishList)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "user",
        "created_at",
        "updated_at",
    )
