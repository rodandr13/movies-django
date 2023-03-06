from django.contrib import admin

from .models import (Category, Genre, Movie, MovieShots, Actor, Rating,
                     RatingStar, Reviews)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "url", "draft")
    list_display_links = ("title",)
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster")
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fess_in_usa", "fess_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        })
    )


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "parent", "movie")
    list_display_links = ("email",)
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description")
    list_display_links = ("title",)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "age")
    list_display_links = ("name",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "ip", "star")
    list_display_links = ("ip",)


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ("id", "value")
    list_display_links = ("value",)
