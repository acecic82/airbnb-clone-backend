from django.db import models

# Create your models here.


class CommonModel(models.Model):
    """Common Model Definition"""

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.name

    """이 class 는 장고에서 모델을 configure 할 때 사용"""

    class Meta:
        abstract = True
