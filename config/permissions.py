from strawberry.permission import BasePermission
from strawberry.types import Info
import typing
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
