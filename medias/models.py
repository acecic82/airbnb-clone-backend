from django.db import models

from common.models import CommonModel

# Create your models here.


class Photo(CommonModel):
    """Photo Model Definition"""

    file = models.URLField()
    description = models.CharField(
        max_length=140,
    )
    room = models.ForeignKey(
        "rooms.Room",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="photos",
    )
    experience = models.ForeignKey(
        "experiences.Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="experiences",
    )

    def __str__(self):
        return "Photo file"


class Video(CommonModel):
    """Video Model Definition"""

    file = models.URLField()
    experience = models.OneToOneField(
        "experiences.Experience",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Photo file"
