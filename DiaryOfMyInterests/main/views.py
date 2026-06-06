from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .forms import (BookForm, FilmForm, RestaurantForm, EventForm, GameForm, SeriesForm, MusicForm,)
from .recommendations import get_recommendations
from typing import Type
from django.db.models import Model
from collections import Counter
from rest_framework import viewsets
from .models import (Book, Film, Restaurant, Event, Game, Series, Music,)
from .serializers import (BookSerializer, FilmSerializer, RestaurantSerializer, EventSerializer,
BookReviewSerializer, FilmReviewSerializer, RestaurantReviewSerializer, EventReviewSerializer)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import (BookReview, FilmReview, RestaurantReview, EventReview, GameReview, SeriesReview, MusicReview,)
from .serializers import MyReviewSerializer

@login_required
def home(request):

    user = request.user
    reviews = []

    # =====================================================
    # ОТЗЫВЫ С OPTIMIZATION
    # =====================================================

    book_reviews = BookReview.objects.filter(user=user)\
        .select_related('book')\
        .prefetch_related('book__tags')

    film_reviews = FilmReview.objects.filter(user=user)\
        .select_related('film')\
        .prefetch_related('film__tags')

    restaurant_reviews = RestaurantReview.objects.filter(user=user)\
        .select_related('restaurant')\
        .prefetch_related('restaurant__tags')

    event_reviews = EventReview.objects.filter(user=user)\
        .select_related('event')

    game_reviews = GameReview.objects.filter(user=user)\
        .select_related('game')\
        .prefetch_related(
            'game__game_genres',
            'game__settings'
        )

    series_reviews = SeriesReview.objects.filter(user=user)\
        .select_related('series')\
        .prefetch_related('series__tags')

    music_reviews = MusicReview.objects.filter(user=user)\
        .select_related('music')\
        .prefetch_related('music__tags')

    # =====================================================
    # СОБИРАЕМ ВСЕ ОТЗЫВЫ
    # =====================================================

    for review in book_reviews:
        reviews.append({
            'type': 'book',
            'review': review,
            'object': review.book
        })

    for review in film_reviews:
        reviews.append({
            'type': 'film',
            'review': review,
            'object': review.film
        })

    for review in restaurant_reviews:
        reviews.append({
            'type': 'restaurant',
            'review': review,
            'object': review.restaurant
        })

    for review in event_reviews:
        reviews.append({
            'type': 'event',
            'review': review,
            'object': review.event
        })

    for review in game_reviews:
        reviews.append({
            'type': 'game',
            'review': review,
            'object': review.game
        })

    for review in series_reviews:
        reviews.append({
            'type': 'series',
            'review': review,
            'object': review.series
        })

    for review in music_reviews:
        reviews.append({
            'type': 'music',
            'review': review,
            'object': review.music
        })

    reviews.sort(
        key=lambda x: x['review'].date,
        reverse=True
    )

    # =====================================================
    # РЕКОМЕНДАЦИИ
    # =====================================================

    recommendations = get_recommendations(user)

    # =====================================================
    # КОЛИЧЕСТВО ОТЗЫВОВ
    # =====================================================

    review_count = (
        len(book_reviews) +
        len(film_reviews) +
        len(restaurant_reviews) +
        len(event_reviews) +
        len(game_reviews) +
        len(series_reviews) +
        len(music_reviews)
    )

    category_counts = {
        'Книги': len(book_reviews),
        'Фильмы': len(film_reviews),
        'Заведения': len(restaurant_reviews),
        'Мероприятия': len(event_reviews),
        'Игры': len(game_reviews),
        'Сериалы': len(series_reviews),
        'Музыка': len(music_reviews),
    }

    max_reviews = max(category_counts.values())

    favorite_categories = [
        cat for cat, count in category_counts.items()
        if count == max_reviews and count > 0
    ]

    # =====================================================
    # ЛЮБИМЫЕ ТЕГИ
    # =====================================================

    all_tags = []

    for review in book_reviews:
        all_tags.extend([
            tag.name for tag in review.book.tags.all()
        ])

    for review in film_reviews:
        all_tags.extend([
            tag.name for tag in review.film.tags.all()
        ])

    for review in restaurant_reviews:
        all_tags.extend([
            tag.name for tag in review.restaurant.tags.all()
        ])

    for review in game_reviews:

        all_tags.extend([
            tag.name for tag in review.game.game_genres.all()
        ])

        all_tags.extend([
            tag.name for tag in review.game.settings.all()
        ])

    for review in series_reviews:
        all_tags.extend([
            tag.name for tag in review.series.tags.all()
        ])

    for review in music_reviews:
        all_tags.extend([
            tag.name for tag in review.music.tags.all()
        ])

    favorite_genres = []

    if all_tags:

        counts = Counter(all_tags)

        max_count = max(counts.values())

        favorite_genres = [
            tag for tag, count in counts.items()
            if count == max_count
        ]

    category_map = {
        'book': 'Книги',
        'film': 'Фильмы',
        'game': 'Игры',
        'series': 'Сериалы',
        'music': 'Музыка',
        'restaurant': 'Заведения',
        'event': 'Мероприятия',
    }

    survey_categories = [
        category_map.get(cat, cat)
        for cat in user.favorite_categories
    ]

    survey_tags = list(
        user.favorite_tags.values_list(
            'name',
            flat=True
        )
    )

    favorite_categories = list(
        dict.fromkeys(
            favorite_categories +
            survey_categories
        )
    )

    favorite_genres = list(
        dict.fromkeys(
            favorite_genres +
            survey_tags
        )
    )

    return render(request, 'main/main.html', {
        'user_email': user.email,
        'reviews': reviews,
        'recommendations': recommendations,
        'book_form': BookForm(),
        'film_form': FilmForm(),
        'restaurant_form': RestaurantForm(),
        'event_form': EventForm(),
        'game_form': GameForm(),
        'series_form': SeriesForm(),
        'music_form': MusicForm(),
        'review_count': review_count,
        'favorite_categories': favorite_categories,
        'favorite_genres': favorite_genres,
    })


@login_required
def create_review(request, category):

    forms_map = {
        'book': (BookForm, Book, BookReview),
        'film': (FilmForm, Film, FilmReview),
        'restaurant': (RestaurantForm, Restaurant, RestaurantReview),
        'event': (EventForm, Event, EventReview),
        'game': (GameForm, Game, GameReview),
        'series': (SeriesForm, Series, SeriesReview),
        'music': (MusicForm, Music, MusicReview),
    }

    config = forms_map.get(category)

    if not config:
        return redirect('main:home')

    form_class, obj_model, review_model = config

    if request.method != 'POST':
        return redirect('main:home')

    form = form_class(request.POST, request.FILES)

    if not form.is_valid():
        return redirect('main:home')

    cleaned_data = form.cleaned_data

    # =====================================================
    # ОБЪЕКТ
    # =====================================================

    name = cleaned_data.get('name')

    obj_instance = obj_model.objects.filter(name=name).first()

    if not obj_instance:
        obj_instance = obj_model.objects.create(name=name)

    # =====================================================
    # ОБНОВЛЕНИЕ ПОЛЕЙ
    # =====================================================

    excluded_fields = {
        'tags',
        'game_genres',
        'settings'
    }

    updated = False

    for field, value in cleaned_data.items():

        if field in excluded_fields:
            continue

        if value and getattr(obj_instance, field) != value:

            setattr(obj_instance, field, value)
            updated = True

    if updated:
        obj_instance.save()

    # =====================================================
    # MANY TO MANY
    # =====================================================

    m2m_fields = [
        'tags',
        'game_genres',
        'settings'
    ]

    for field in m2m_fields:

        if hasattr(obj_instance, field) and field in cleaned_data:

            getattr(obj_instance, field).set(
                cleaned_data[field]
            )

    review_model.objects.create(
        user=request.user,
        rating=request.POST.get('rating', 0),
        full_text=request.POST.get('full_text', ''),
        **{category: obj_instance}
    )

    return redirect('main:home')


@login_required
def delete_review(request, category: str, pk: int):
    """Удаление отзыва пользователя без удаления объекта"""
    review_models: dict[str, Type[Model]] = {
        'book': BookReview,
        'film': FilmReview,
        'restaurant': RestaurantReview,
        'event': EventReview,
        'game': GameReview,
        'series': SeriesReview,
        'music': MusicReview,
    }
    review_model = review_models.get(category)
    if not review_model:
        return redirect('main:home')

    review = review_model.objects.filter(pk=pk, user=request.user).first()
    if request.method == 'POST' and review:
        review.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

    return redirect('main:home')


@login_required
def edit_review_form(request, category, pk):
    review_models = {
        'book': BookReview,
        'film': FilmReview,
        'restaurant': RestaurantReview,
        'event': EventReview,
        'game': GameReview,
        'series': SeriesReview,
        'music': MusicReview,
    }

    review_model = review_models.get(category)
    if not review_model:
        return JsonResponse({'error': 'invalid category'}, status=400)

    review = get_object_or_404(review_model, pk=pk, user=request.user)

    return JsonResponse({
        'rating': review.rating,
        'full_text': review.full_text,
    })


@login_required
def edit_review(request, category, pk):

    review_models = {
        'book': BookReview,
        'film': FilmReview,
        'restaurant': RestaurantReview,
        'event': EventReview,
        'game': GameReview,
        'series': SeriesReview,
        'music': MusicReview,
    }

    review_model = review_models.get(category)
    if not review_model:
        return redirect('main:home')

    review = get_object_or_404(review_model, pk=pk, user=request.user)

    if request.method == 'POST':
        review.rating = request.POST.get('rating')
        review.full_text = request.POST.get('full_text')
        review.save()

    return redirect('main:home')


@login_required
def get_object_reviews(request, category, pk):
    review_models = {
        'book': BookReview,
        'film': FilmReview,
        'restaurant': RestaurantReview,
        'event': EventReview,
        'game': GameReview,
        'series': SeriesReview,
        'music': MusicReview,
    }

    object_models = {
        'book': Book,
        'film': Film,
        'restaurant': Restaurant,
        'event': Event,
        'game': Game,
        'series': Series,
        'music': Music,
    }

    review_model = review_models.get(category)
    obj_model = object_models.get(category)

    if not review_model or not obj_model:
        return JsonResponse({'html': ''})

    obj_instance = get_object_or_404(obj_model, pk=pk)

    filter_kwargs = {category: obj_instance}

    reviews = review_model.objects.filter(
        **filter_kwargs
    ).select_related('user')

    reviews_list = [
        {
            'review': review,
            'type': category
        }
        for review in reviews
    ]

    html = render_to_string(
        'main/object_reviews_panel.html',
        {
            'reviews': reviews_list
        },
        request=request
    )

    return JsonResponse({
        'html': html
    })

@login_required
def profile_data(request):
    user = request.user
    book_reviews = BookReview.objects.filter(user=user)
    film_reviews = FilmReview.objects.filter(user=user)
    restaurant_reviews = RestaurantReview.objects.filter(user=user)
    event_reviews = EventReview.objects.filter(user=user)
    game_reviews = GameReview.objects.filter(user=user)
    series_reviews = SeriesReview.objects.filter(user=user)
    music_reviews = MusicReview.objects.filter(user=user)

    review_count = (
        book_reviews.count() +
        film_reviews.count() +
        restaurant_reviews.count() +
        event_reviews.count() +
        game_reviews.count() +
        series_reviews.count() +
        music_reviews.count()
    )

    category_counts = {
        'Книги': book_reviews.count(),
        'Фильмы': film_reviews.count(),
        'Заведения': restaurant_reviews.count(),
        'Мероприятия': event_reviews.count(),
        'Игры': game_reviews.count(),
        'Сериалы': series_reviews.count(),
        'Музыка': music_reviews.count(),
    }

    max_reviews = max(category_counts.values())

    favorite_categories = [
        cat for cat, count in category_counts.items()
        if count == max_reviews and count > 0
    ]
    all_tags = []

    for review in book_reviews:
        all_tags.extend(
            review.book.tags.values_list('name', flat=True)
        )

    for review in film_reviews:
        all_tags.extend(
            review.film.tags.values_list('name', flat=True)
        )

    for review in restaurant_reviews:
        all_tags.extend(
            review.restaurant.tags.values_list('name', flat=True)
        )

    for review in game_reviews:
        all_tags.extend(
            review.game.tags.values_list('name', flat=True)
        )

    for review in series_reviews:
        all_tags.extend(
            review.series.tags.values_list('name', flat=True)
        )

    for review in music_reviews:
        all_tags.extend(
            review.music.tags.values_list('name', flat=True)
        )
    favorite_genres = []

    if all_tags:
        counts = Counter(all_tags)
        max_count = max(counts.values())

        favorite_genres = [
            tag for tag, count in counts.items()
            if count == max_count
        ]

    survey_categories = user.favorite_categories

    survey_tags = list(
        user.favorite_tags.values_list(
            'name',
            flat=True
        )
    )

    favorite_categories = list(
        set(favorite_categories + survey_categories)
    )

    favorite_genres = list(
        set(favorite_genres + survey_tags)
    )

    return {
        'review_count': review_count,
        'favorite_categories': favorite_categories,
        'favorite_genres': favorite_genres,
    }

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class BookReviewViewSet(viewsets.ModelViewSet):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer


class FilmReviewViewSet(viewsets.ModelViewSet):
    queryset = FilmReview.objects.all()
    serializer_class = FilmReviewSerializer


class RestaurantReviewViewSet(viewsets.ModelViewSet):
    queryset = RestaurantReview.objects.all()
    serializer_class = RestaurantReviewSerializer


class EventReviewViewSet(viewsets.ModelViewSet):
    queryset = EventReview.objects.all()
    serializer_class = EventReviewSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_reviews(request):

    user = request.user
    reviews = []

    review_configs = [
        (
            BookReview.objects.filter(user=user).select_related('book'),
            'book',
            'book',
            'cover'
        ),
        (
            FilmReview.objects.filter(user=user).select_related('film'),
            'film',
            'film',
            'cover'
        ),
        (
            RestaurantReview.objects.filter(user=user).select_related('restaurant'),
            'restaurant',
            'restaurant',
            'photo'
        ),
        (
            EventReview.objects.filter(user=user).select_related('event'),
            'event',
            'event',
            'photo'
        ),
        (
            GameReview.objects.filter(user=user).select_related('game'),
            'game',
            'game',
            'cover'
        ),
        (
            SeriesReview.objects.filter(user=user).select_related('series'),
            'series',
            'series',
            'cover'
        ),
        (
            MusicReview.objects.filter(user=user).select_related('music'),
            'music',
            'music',
            'cover'
        ),
    ]

    for queryset, review_type, field_name, image_field in review_configs:

        for r in queryset:

            obj = getattr(r, field_name)
            image = getattr(obj, image_field)

            reviews.append({
                "id": r.id,
                "review_type": review_type,
                "title": obj.name,
                "text": r.full_text or "",
                "rating": r.rating,
                "date": r.date,
                "cover": image.url if image else ""
            })

    reviews.sort(
        key=lambda x: x["date"],
        reverse=True
    )

    reviews = reviews[:20]

    serializer = MyReviewSerializer(
        reviews,
        many=True
    )

    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_review(request, review_type, review_id):

    if review_type == "book":
        review = BookReview.objects.get(id=review_id, user=request.user)

    elif review_type == "film":
        review = FilmReview.objects.get(id=review_id, user=request.user)

    elif review_type == "restaurant":
        review = RestaurantReview.objects.get(id=review_id, user=request.user)

    elif review_type == "event":
        review = EventReview.objects.get(id=review_id, user=request.user)

    else:
        return Response({"error": "invalid type"}, status=400)

    review.rating = request.data.get("rating")
    review.full_text = request.data.get("full_text")
    review.save()

    return Response({"status": "ok"})

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_review_api(request, review_type, review_id):

    model_map = {
        "book": BookReview,
        "film": FilmReview,
        "restaurant": RestaurantReview,
        "event": EventReview
    }

    model = model_map.get(review_type)

    if not model:
        return Response({"error": "Неверный тип"}, status=400)

    try:
        review = model.objects.get(id=review_id, user=request.user)

        review.delete()  # ← ВОТ ГЛАВНАЯ СТРОКА

        return Response({"status": "deleted"})

    except model.DoesNotExist:
        return Response({"error": "Отзыв не найден"}, status=404)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review_api(request, review_type):

    data = request.data
    user = request.user

    review_configs = {
        "film": {
            "model": Film,
            "serializer": FilmReviewSerializer,
            "field": "film",
            "name_field": "film_name",
            "image_field": "cover"
        },
        "book": {
            "model": Book,
            "serializer": BookReviewSerializer,
            "field": "book",
            "name_field": "book_name",
            "image_field": "cover"
        },
        "restaurant": {
            "model": Restaurant,
            "serializer": RestaurantReviewSerializer,
            "field": "restaurant",
            "name_field": "restaurant_name",
            "image_field": "photo"
        },
        "event": {
            "model": Event,
            "serializer": EventReviewSerializer,
            "field": "event",
            "name_field": "event_name",
            "image_field": "photo"
        },
    }

    config = review_configs.get(review_type)

    if not config:
        return Response(
            {"error": "Неверный тип"},
            status=400
        )

    name = data.get(config["name_field"])
    if not name:
        return Response(
            {
                config["name_field"]: "Обязательное поле"
            },
            status=400
        )

    model = config["model"]
    obj = model.objects.filter(name=name).first()
    if not obj:
        obj = model.objects.create(name=name)

    image_file = request.FILES.get("cover")
    if image_file:
        setattr(
            obj,
            config["image_field"],
            image_file
        )
        obj.save()

    review_data = {
        config["field"]: obj.id,
        "user": user.id,
        "rating": int(data.get("rating", 0)),
        "full_text": data.get("review_text", "")
    }

    serializer = config["serializer"](data=review_data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            serializer.data,
            status=201
        )
    return Response(
        serializer.errors,
        status=400
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_recommendations(request):

    user = request.user
    recommendations = get_recommendations(user)
    result = []
    for r in recommendations[:20]:
        obj = r["obj"]
        cover = ""
        if hasattr(obj, "cover") and obj.cover:
            cover = obj.cover.url
        elif hasattr(obj, "photo") and obj.photo:
            cover = obj.photo.url

        result.append({
            "type": r["type"],
            "title": obj.name,
            "avg_rating": r["avg_rating"],
            "cover": cover
        })

    return Response(result)


