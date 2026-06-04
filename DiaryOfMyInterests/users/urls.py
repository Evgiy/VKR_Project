from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from .views import UserRegisterView
from .views import UserLoginView
from .views import CurrentUserView

app_name = 'users'
router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', views.registration, name='registration'),
    path('login/', views.login_view, name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('api/login/', UserLoginView.as_view(), name='api_login'),
    path('api/current_user/', CurrentUserView.as_view(), name='current_user'),
]

urlpatterns += router.urls