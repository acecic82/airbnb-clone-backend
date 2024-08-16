from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    # 순서에 따라 me를 username 으로 인식할 수도 있음
    path("@<str:username>", views.PublicUser.as_view()),
]
