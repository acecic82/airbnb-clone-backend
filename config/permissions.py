from strawberry.permission import BasePermission
from strawberry.types import Info
import typing
import jwt
from .settings import SECRET_KEY
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class OnlyLoggedIn(BasePermission):
    message = "You need to be logged in for this!"

    def has_permission(self, source: typing.Any, info: Info):
        return info.context.request.user.is_authenticated


class TrustMeBroAuthentication(BaseAuthentication):
    def authenticate(self, request):
        username = request.headers.get("Trust-Me")
        if not username:
            return None
        try:
            user = User.objects.get(username=username)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed(f"No user {username}")


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):

        token = request.headers.get("Jwt-Token")

        if not token:
            return None

        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"],
        )
        pk = decoded.get("pk")

        if not pk:
            raise AuthenticationFailed("Invalid Token")

        try:
            user = User.objects.get(pk=pk)
            return (user, None)
        except User.DoesNotExist:
            raise AuthenticationFailed("User Not Found")
