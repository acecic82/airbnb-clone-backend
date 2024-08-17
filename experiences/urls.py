from django.urls import path
from . import views

urlpatterns = [
    path("", views.Experiences.as_view()),
    path("<int:experience_pk>", views.ExperienceDetail.as_view()),
    path("perks/", views.Perks.as_view()),
    path("perks/<int:perk_id>", views.PerkDetail.as_view()),
]
