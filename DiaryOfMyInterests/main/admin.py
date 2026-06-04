from django.contrib import admin
from .models import (
    Tag,
    Book, BookReview,
    Film, FilmReview,
    Restaurant, RestaurantReview,
    Event, EventReview,
    Game, GameReview,
    Series, SeriesReview,
    Music, MusicReview,
)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'cover')
    search_fields = ('name', 'author', 'genre')
    filter_horizontal = ('tags',)

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('bookname', 'user__username', 'full_text')

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director', 'cover')
    search_fields = ('name', 'director', 'genre')
    filter_horizontal = ('tags',)

@admin.register(FilmReview)
class FilmReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'film', 'user', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('film__name', 'user__username', 'full_text')

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'photo')
    search_fields = ('name', 'address', 'cuisine')
    filter_horizontal = ('tags',)

@admin.register(RestaurantReview)
class RestaurantReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'user', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('restaurant__name', 'user__username', 'full_text')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'photo')
    search_fields = ('name', 'address')

@admin.register(EventReview)
class EventReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'user', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('event__name', 'user__username', 'full_text')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'developer', 'publisher', 'cover')
    search_fields = ('name', 'genre', 'developer', 'publisher')
    filter_horizontal = ('game_genres', 'settings')


@admin.register(GameReview)
class GameReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'game', 'user', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('game__name', 'user__username', 'full_text')

@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'showrunner', 'cover')
    search_fields = ('name', 'genre', 'showrunner')
    filter_horizontal = ('tags',)


@admin.register(SeriesReview)
class SeriesReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'series', 'user', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('series__name', 'user__username', 'full_text')

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'artist', 'cover')
    search_fields = ('name', 'artist', 'genre')
    filter_horizontal = ('tags',)


@admin.register(MusicReview)
class MusicReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'music', 'user', 'rating', 'date')
    list_filter = ('rating', 'date')
    search_fields = ('music__name', 'user__username', 'full_text')