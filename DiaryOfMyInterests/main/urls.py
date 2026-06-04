from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet, FilmViewSet, RestaurantViewSet, EventViewSet,
    BookReviewViewSet, FilmReviewViewSet,
    RestaurantReviewViewSet, EventReviewViewSet
)
from .views import my_reviews, update_review, delete_review_api, create_review_api, my_recommendations

app_name = 'main'

router = DefaultRouter()

router.register(r'books', BookViewSet)
router.register(r'films', FilmViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'events', EventViewSet)

router.register(r'book-reviews', BookReviewViewSet)
router.register(r'film-reviews', FilmReviewViewSet)
router.register(r'restaurant-reviews', RestaurantReviewViewSet)
router.register(r'event-reviews', EventReviewViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('create/<str:category>/', views.create_review, name='create_review'),
    path('delete/<str:category>/<int:pk>/', views.delete_review, name='delete_review'),
    path('edit_form/<str:category>/<int:pk>/', views.edit_review_form, name='edit_review_form'),
    path('edit/<str:category>/<int:pk>/', views.edit_review, name='edit_review'),
    path('reviews/<str:category>/<int:pk>/', views.get_object_reviews, name='get_object_reviews'),
    path('api/my_reviews/', my_reviews, name='my_reviews'),
    path('api/review/<str:review_type>/<int:review_id>/', update_review),
    path('api/delete_review/<str:review_type>/<int:review_id>/', delete_review_api),
    path('api/create_review/<str:review_type>/', create_review_api),
    path('api/my_recommendations/', my_recommendations),
]

urlpatterns += router.urls