from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("log-in", views.LogIn.as_view()),
    path("log-out", views.LogOut.as_view()),
    path("token-login", obtain_auth_token),
    path("jwt-login", views.JWTLogIn.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    # 순서에 따라 me를 username 으로 인식할 수도 있음
    path("@<str:username>", views.PublicUser.as_view()),
]
