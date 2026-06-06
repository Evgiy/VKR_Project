from django.db.models import Avg, Count, Q
from .models import (
    Book, BookReview,
    Film, FilmReview,
    Restaurant, RestaurantReview,
    Event, EventReview,
    Game, GameReview,
    Series, SeriesReview,
    Music, MusicReview
)

def get_user_recommendations(user):
    recommendations = []
    favorite_book_tags = Book.objects.filter(
        reviews__user=user,
        reviews__rating__gte=4
    ).values_list('tags', flat=True)

    favorite_film_tags = Film.objects.filter(
        reviews__user=user,
        reviews__rating__gte=4
    ).values_list('tags', flat=True)

    favorite_game_genres = Game.objects.filter(
        reviews__user=user,
        reviews__rating__gte=4
    ).values_list('game_genres', flat=True)

    favorite_game_settings = Game.objects.filter(
        reviews__user=user,
        reviews__rating__gte=4
    ).values_list('settings', flat=True)

    favorite_series_tags = Series.objects.filter(
        reviews__user=user,
        reviews__rating__gte=4
    ).values_list('tags', flat=True)

    favorite_music_tags = Music.objects.filter(
        reviews__user=user,
        reviews__rating__gte=4
    ).values_list('tags', flat=True)

    favorite_restaurant_tags = Restaurant.objects.filter(
        reviews__user=user,
        reviews__rating__gte=4
    ).values_list('tags', flat=True)

    favorite_authors = Book.objects.filter(
        reviews__user=user,
        reviews__rating__gte=4
    ).values_list('author', flat=True)

    favorite_directors = Film.objects.filter(
        reviews__user=user,
        reviews__rating__gte=4
    ).values_list('director', flat=True)

    favorite_developers = Game.objects.filter(
        reviews__user=user,
        reviews__rating__gte=4
    ).values_list('developer', flat=True)

    favorite_publishers = Game.objects.filter(
        reviews__user=user,
        reviews__rating__gte=4
    ).values_list('publisher', flat=True)

    favorite_showrunners = Series.objects.filter(
        reviews__user=user,
        reviews__rating__gte=4
    ).values_list('showrunner', flat=True)

    favorite_artists = Music.objects.filter(
        reviews__user=user,
        reviews__rating__gte=4
    ).values_list('artist', flat=True)

    books = Book.objects.filter(
        Q(tags__in=favorite_book_tags) |
        Q(author__in=favorite_authors)
    ).exclude(
        reviews__user=user
    ).annotate(
        review_count=Count('reviews')
    ).filter(
        review_count__gt=0
    ).distinct()

    for book in books:
        avg_rating = BookReview.objects.filter(
            book=book
        ).aggregate(avg=Avg('rating'))['avg']
        recommendations.insert(0,{
            'type': 'book',
            'obj': book,
            'avg_rating': round(avg_rating, 1)
        })

    films = Film.objects.filter(
        Q(tags__in=favorite_film_tags) |
        Q(director__in=favorite_directors)
    ).exclude(
        reviews__user=user
    ).annotate(
        review_count=Count('reviews')
    ).filter(
        review_count__gt=0
    ).distinct()

    for film in films:
        avg_rating = FilmReview.objects.filter(
            film=film
        ).aggregate(avg=Avg('rating'))['avg']
        recommendations.insert(0,{
            'type': 'film',
            'obj': film,
            'avg_rating': round(avg_rating, 1)
        })

    games = Game.objects.filter(
        Q(game_genres__in=favorite_game_genres) |
        Q(settings__in=favorite_game_settings) |
        Q(developer__in=favorite_developers) |
        Q(publisher__in=favorite_publishers)
    ).exclude(
        reviews__user=user
    ).annotate(
        review_count=Count('reviews')
    ).filter(
        review_count__gt=0
    ).distinct()

    for game in games:
        avg_rating = GameReview.objects.filter(
            game=game
        ).aggregate(avg=Avg('rating'))['avg']
        recommendations.insert(0,{
            'type': 'game',
            'obj': game,
            'avg_rating': round(avg_rating, 1)
        })

    series_list = Series.objects.filter(
        Q(tags__in=favorite_series_tags) |
        Q(showrunner__in=favorite_showrunners)
    ).exclude(
        reviews__user=user
    ).annotate(
        review_count=Count('reviews')
    ).filter(
        review_count__gt=0
    ).distinct()

    for series in series_list:
        avg_rating = SeriesReview.objects.filter(
            series=series
        ).aggregate(avg=Avg('rating'))['avg']
        recommendations.insert(0,{
            'type': 'series',
            'obj': series,
            'avg_rating': round(avg_rating, 1)
        })

    music_list = Music.objects.filter(
        Q(tags__in=favorite_music_tags) |
        Q(artist__in=favorite_artists)
    ).exclude(
        reviews__user=user
    ).annotate(
        review_count=Count('reviews')
    ).filter(
        review_count__gt=0
    ).distinct()

    for music in music_list:
        avg_rating = MusicReview.objects.filter(
            music=music
        ).aggregate(avg=Avg('rating'))['avg']
        recommendations.insert(0,{
            'type': 'music',
            'obj': music,
            'avg_rating': round(avg_rating, 1)
        })

    restaurants = Restaurant.objects.filter(
        tags__in=favorite_restaurant_tags
    ).exclude(
        reviews__user=user
    ).annotate(
        review_count=Count('reviews')
    ).filter(
        review_count__gt=0
    ).distinct()

    for restaurant in restaurants:
        avg_rating = RestaurantReview.objects.filter(
            restaurant=restaurant
        ).aggregate(avg=Avg('rating'))['avg']
        recommendations.insert(0,{
            'type': 'restaurant',
            'obj': restaurant,
            'avg_rating': round(avg_rating, 1)
        })

    events = Event.objects.exclude(
        reviews__user=user
    ).annotate(
        review_count=Count('reviews')
    ).filter(
        review_count__gt=0
    ).distinct()

    for event in events:
        avg_rating = EventReview.objects.filter(
            event=event
        ).aggregate(avg=Avg('rating'))['avg']
        recommendations.insert(0,{
            'type': 'event',
            'obj': event,
            'avg_rating': round(avg_rating, 1)
        })

    return recommendations

def get_survey_recommendations(user):

    recommendations = []

    categories = user.favorite_categories
    tags = user.favorite_tags.all()

    if not categories or not tags.exists():
        return recommendations

    if "book" in categories:

        books = Book.objects.filter(
            tags__in=tags
        ).distinct()[:10]

        for book in books:
            avg = BookReview.objects.filter(
                book=book
            ).aggregate(
                avg=Avg('rating')
            )['avg'] or 0

            recommendations.append({
                'type': 'book',
                'obj': book,
                'avg_rating': round(avg, 1)
            })

    if "film" in categories:

        films = Film.objects.filter(
            tags__in=tags
        ).distinct()[:10]

        for film in films:
            avg = FilmReview.objects.filter(
                film=film
            ).aggregate(
                avg=Avg('rating')
            )['avg'] or 0

            recommendations.append({
                'type': 'film',
                'obj': film,
                'avg_rating': round(avg, 1)
            })

    if "game" in categories:

        games = Game.objects.filter(
            Q(game_genres__in=tags) |
            Q(settings__in=tags)
        ).distinct()[:10]

        for game in games:
            avg = GameReview.objects.filter(
                game=game
            ).aggregate(
                avg=Avg('rating')
            )['avg'] or 0

            recommendations.append({
                'type': 'game',
                'obj': game,
                'avg_rating': round(avg, 1)
            })

    if "series" in categories:

        series_list = Series.objects.filter(
            tags__in=tags
        ).distinct()[:10]

        for series in series_list:
            avg = SeriesReview.objects.filter(
                series=series
            ).aggregate(
                avg=Avg('rating')
            )['avg'] or 0

            recommendations.append({
                'type': 'series',
                'obj': series,
                'avg_rating': round(avg, 1)
            })

    if "music" in categories:

        music_list = Music.objects.filter(
            tags__in=tags
        ).distinct()[:10]

        for music in music_list:
            avg = MusicReview.objects.filter(
                music=music
            ).aggregate(
                avg=Avg('rating')
            )['avg'] or 0

            recommendations.append({
                'type': 'music',
                'obj': music,
                'avg_rating': round(avg, 1)
            })

    if "restaurant" in categories:

        restaurants = Restaurant.objects.filter(
            tags__in=tags
        ).distinct()[:10]

        for restaurant in restaurants:
            avg = RestaurantReview.objects.filter(
                restaurant=restaurant
            ).aggregate(
                avg=Avg('rating')
            )['avg'] or 0

            recommendations.append({
                'type': 'restaurant',
                'obj': restaurant,
                'avg_rating': round(avg, 1)
            })

    if "event" in categories:

        events = Event.objects.all()[:10]

        for event in events:
            avg = EventReview.objects.filter(
                event=event
            ).aggregate(
                avg=Avg('rating')
            )['avg'] or 0

            recommendations.append({
                'type': 'event',
                'obj': event,
                'avg_rating': round(avg, 1)
            })

    return recommendations

def get_recommendations(user):

    classic = get_user_recommendations(user)

    if classic:
        return classic

    return get_survey_recommendations(user)