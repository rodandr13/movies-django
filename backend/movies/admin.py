from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import (Category, Genre, Movie, MovieShots, Actor, Rating,
                     RatingStar, Reviews)


class MovieAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label="Описание",
                                  widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label="Description",
                                  widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} height="100" />')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    list_display = ("id", "title", "category", "url", "draft")
    list_display_links = ("title",)
    list_filter = ("category", "year")
    form = MovieAdminForm
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewInline]
    actions = ["publish", "unpublish"]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
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
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} height="100" />')

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлена"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлена"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ("change",)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ("change",)

    get_image.short_description = "Изображение"


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "parent", "movie")
    list_display_links = ("email",)
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


@admin.register(MovieShots)
class MovieShotsAdmin(TranslationAdmin):
    list_display = ("id", "title", "description", "get_image")
    list_display_links = ("title",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} height="100" />')

    get_image.short_description = "Изображение"


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    list_display = ("id", "name", "age", "get_image")
    list_display_links = ("name",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} height="100" />')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id", "ip", "star")
    list_display_links = ("ip",)


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ("id", "value")
    list_display_links = ("value",)


admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
