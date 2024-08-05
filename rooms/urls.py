from django.urls import path
from . import views

urlpatterns = [
    path("", views.see_all_room),
    path("<int:room_id>", views.see_one_room),
    path("amenities", views.Amenities.as_view()),
    path("amenities/<int:amenity_id>", views.AmenityDeatil.as_view()),
]
