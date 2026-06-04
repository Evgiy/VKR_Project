from django import forms
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

class BaseReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5, required=True, label='Оценка')
    full_text = forms.CharField(widget=forms.Textarea, required=False, label='Отзыв')

class BookReviewForm(BaseReviewForm):
    class Meta:
        model = BookReview
        fields = ('rating', 'full_text')

class FilmReviewForm(BaseReviewForm):
    class Meta:
        model = FilmReview
        fields = ('rating', 'full_text')

class RestaurantReviewForm(BaseReviewForm):
    class Meta:
        model = RestaurantReview
        fields = ('rating', 'full_text')

class EventReviewForm(BaseReviewForm):
    class Meta:
        model = EventReview
        fields = ('rating', 'full_text')

class GameReviewForm(BaseReviewForm):
    class Meta:
        model = GameReview
        fields = ('rating', 'full_text')

class SeriesReviewForm(BaseReviewForm):
    class Meta:
        model = SeriesReview
        fields = ('rating', 'full_text')

class MusicReviewForm(BaseReviewForm):
    class Meta:
        model = MusicReview
        fields = ('rating', 'full_text')

class BookForm(forms.ModelForm):
    cover = forms.ImageField(required=False, label='', widget=forms.FileInput(attrs={'style':'display:none'}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(type='genre'),
        widget=forms.SelectMultiple(attrs={'id':'bookTags'}),
        required=False,
        label='Жанр')

    class Meta:
        model = Book
        fields = ('name', 'author', 'cover', 'tags')


class FilmForm(forms.ModelForm):
    cover = forms.ImageField(required=False, label='', widget=forms.FileInput(attrs={'style':'display:none'}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(type='genre'),
        widget=forms.SelectMultiple(attrs={'id':'filmTags'}),
        required=False,
        label='Жанр')
    class Meta:
        model = Film
        fields = ('name', 'director', 'cover', 'tags')


class RestaurantForm(forms.ModelForm):
    photo = forms.ImageField(required=False, label='', widget=forms.FileInput(attrs={'style':'display:none'}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(type='cuisine'),
        widget=forms.SelectMultiple(attrs={'id':'restaurantTags'}),
        required=False,
        label='Кухня')
    class Meta:
        model = Restaurant
        fields = ('name', 'address', 'photo', 'tags')


class EventForm(forms.ModelForm):
    photo = forms.ImageField(required=False, label='', widget=forms.FileInput(attrs={'style':'display:none'}))
    class Meta:
        model = Event
        fields = ('name', 'address', 'photo')


class GameForm(forms.ModelForm):
    cover = forms.ImageField(required=False, label='', widget=forms.FileInput(attrs={'style':'display:none'}))
    game_genres = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(type='game_genre'),
        widget=forms.SelectMultiple(attrs={'id':'gameGenres'}),
        required=False,
        label='Жанр')
    settings = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(type='setting'),
        widget=forms.SelectMultiple(attrs={'id':'gameSettings'}),
        required=False,
        label='Cеттинг')
    class Meta:
        model = Game
        fields = ('name', 'developer', 'publisher', 'cover', 'game_genres', 'settings')


class SeriesForm(forms.ModelForm):
    cover = forms.ImageField(required=False, label='', widget=forms.FileInput(attrs={'style':'display:none'}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(type='genre'),
        widget=forms.SelectMultiple(attrs={'id':'seriesTags'}),
        required=False,
        label='Жанр')
    class Meta:
        model = Series
        fields = ('name', 'showrunner', 'cover', 'tags')


class MusicForm(forms.ModelForm):
    cover = forms.ImageField(required=False, label='', widget=forms.FileInput(attrs={'style':'display:none'}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(type='music_genre'),
        widget=forms.SelectMultiple(attrs={'id':'musicTags'}),
        required=False,
        label='Жанр')
    class Meta:
        model = Music
        fields = ('name', 'artist', 'cover', 'tags')


