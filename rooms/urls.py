from django.urls import path
from . import views

urlpatterns = [
    path("", views.Rooms.as_view()),
    path("<int:room_id>", views.RoomDeatil.as_view()),
    path("<int:room_id>/reviews", views.RoomReviews.as_view()),
    path("<int:room_id>/amenities", views.RoomAmenities.as_view()),
    path("amenities", views.Amenities.as_view()),
    path("amenities/<int:amenity_id>", views.AmenityDeatil.as_view()),
]
