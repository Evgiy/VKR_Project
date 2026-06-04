from rest_framework import serializers
from .models import (
    Book, Film, Restaurant, Event,
    BookReview, FilmReview, RestaurantReview, EventReview
)

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = '__all__'

class FilmReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmReview
        fields = '__all__'

class RestaurantReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantReview
        fields = '__all__'

class EventReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventReview
        fields = '__all__'

class MyReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    review_type = serializers.CharField()
    title = serializers.CharField()
    text = serializers.CharField()
    rating = serializers.IntegerField()
    date = serializers.DateField()
    cover = serializers.CharField(allow_blank=True)