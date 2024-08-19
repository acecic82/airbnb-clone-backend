import strawberry
import typing

from config.permissions import OnlyLoggedIn
from . import types
from . import queries


@strawberry.type
class Query:
    all_rooms: typing.List[types.RoomType] = strawberry.field(
        resolver=queries.get_all_rooms,
        permission_classes=[OnlyLoggedIn],
    )

    room: typing.Optional[types.RoomType] = strawberry.field(
        resolver=queries.get_room,
    )
