from django.contrib import admin

from reviews.models import Review
from typing import Final


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"

    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("good", "Good"),
            ("great", "Great"),
            ("awesome", "Awesome"),
        ]

    def queryset(self, request, reviews):
        # self.value는 결국 Lookups 의 tuple의 앞에 인자를 가져옴
        word = self.value()
        if word == None:
            return reviews.all()
        return reviews.filter(payload__contains=word)


class GoodOrBadFilter(admin.SimpleListFilter):
    GOOD: Final[str] = "good"
    BAD: Final[str] = "bad"

    title = "Good or Bad Filter"

    parameter_name = "evaluate"

    def lookups(self, request, model_admin):
        return [
            (self.GOOD, "Good"),
            (self.BAD, "Bad"),
        ]

    def queryset(self, request, reviews):
        eval = self.value()

        if eval == self.GOOD:
            print("good case")
            return reviews.filter(rating__gte=3)
        elif eval == self.BAD:
            print("bad case")
            return reviews.filter(rating__lt=3)

        return reviews.all()


# Register your models here.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "payload",
    )

    list_filter = (
        WordFilter,
        GoodOrBadFilter,
        "rating",
        "room__pet_friendly",
    )
