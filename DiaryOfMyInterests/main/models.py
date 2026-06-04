from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL
RATING_CHOICES = [ (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),]

class Tag(models.Model):
    TAG_TYPES = [
        ('genre', 'Жанр'),
        ('game_genre', 'Игровой жанр'),
        ('setting', 'Сеттинг'),
        ('music_genre', 'Музыкальный жанр'),
        ('cuisine', 'Кухня'),
    ]

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20, choices=TAG_TYPES)

    def __str__(self):
        return f"{self.name} ({self.type})"

class Book(models.Model):
    name = models.CharField('Название', max_length=100, db_index=True)
    author = models.CharField('Автор', max_length=100, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='books')
    cover = models.ImageField('Обложка', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES)
    full_text = models.TextField('Отзыв', blank=True, null=True)
    date = models.DateField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.book.name}"

    class Meta:
        verbose_name = 'Отзыв на книгу'
        verbose_name_plural = 'Отзывы на книги'

class Film(models.Model):
    name = models.CharField('Название', max_length=100, db_index=True)
    director = models.CharField('Режиссёр', max_length=100, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='films')
    cover = models.ImageField('Постер', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

class FilmReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES)
    full_text = models.TextField('Отзыв', blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв на фильм'
        verbose_name_plural = 'Отзывы на фильмы'

class Restaurant(models.Model):
    name = models.CharField('Название', max_length=100, db_index=True)
    address = models.CharField('Адрес', max_length=100, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='restaurants')
    photo = models.ImageField('Фото', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'

class RestaurantReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES)
    full_text = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв на ресторан'
        verbose_name_plural = 'Отзывы на рестораны'

class Event(models.Model):
    name = models.CharField('Название', max_length=100, db_index=True)
    address = models.CharField('Адрес', max_length=100, blank=True)
    photo = models.ImageField('Фото', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'

class EventReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')

    rating = models.IntegerField('Оценка', choices=RATING_CHOICES)
    full_text = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв на мероприятие'
        verbose_name_plural = 'Отзывы на мероприятия'

class Game(models.Model):
    name = models.CharField('Название', max_length=100, db_index=True)
    game_genres = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='games_by_genre',
        limit_choices_to={'type': 'game_genre'}
    )
    settings = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='games_by_setting',
        limit_choices_to={'type': 'setting'}
    )
    developer = models.CharField(
        'Разработчик',
        max_length=100,
        blank=True
    )
    publisher = models.CharField(
        'Издатель',
        max_length=100,
        blank=True
    )
    cover = models.ImageField(
        'Обложка',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class GameReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES)
    full_text = models.TextField('Отзыв', blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.game.name}"

    class Meta:
        verbose_name = 'Отзыв на игру'
        verbose_name_plural = 'Отзывы на игры'

class Series(models.Model):
    name = models.CharField('Название', max_length=100, db_index=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='series')
    showrunner = models.CharField('Шоураннер', max_length=100, blank=True)
    cover = models.ImageField('Обложка', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сериал'
        verbose_name_plural = 'Сериалы'


class SeriesReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES)
    full_text = models.TextField('Отзыв', blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.series.name}"

    class Meta:
        verbose_name = 'Отзыв на сериал'
        verbose_name_plural = 'Отзывы на сериалы'

class Music(models.Model):
    name = models.CharField('Название', max_length=100, db_index=True)
    artist = models.CharField('Исполнитель', max_length=100, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='music')
    cover = models.ImageField('Обложка', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Музыка'
        verbose_name_plural = 'Музыка'


class MusicReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField('Оценка', choices=RATING_CHOICES)
    full_text = models.TextField('Отзыв', blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв на музыку'
        verbose_name_plural = 'Отзывы на музыку'

    def __str__(self):
        return f"{self.user} - {self.music.name}"

