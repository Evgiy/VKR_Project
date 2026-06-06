from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from rest_framework import viewsets
from .models import Users
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserRegisterSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from main.models import Tag


def registration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = email.split('@')[0]
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if Users.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с такой почтой уже существует.')
        elif password1 != password2:
            messages.error(request, 'Пароли не совпадают.')
        else:
            user = Users.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('users:survey')

    return render(request, 'users/registration.html')

@login_required
def survey(request):

    return render(
        request,
        'users/survey.html', {'tags': Tag.objects.all()},
    )

@login_required
def save_survey(request):
    if request.method == 'POST':
        categories = request.POST.getlist(
            'categories[]'
        )
        tags = request.POST.getlist(
            'tags[]'
        )
        user = request.user
        user.favorite_categories = categories
        user.save()

        user.favorite_tags.set(
            Tag.objects.filter(
                id__in=tags
            )
        )
        return JsonResponse({
            'success': True
        })
    return JsonResponse({
        'success': False
    })

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('main:home')
        else:
            messages.error(request, 'Неправильная почта или пароль.')

    return render(request, 'users/login.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "email": user.email
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                "token": token.key,
                "email": user.email
            }, status=status.HTTP_200_OK)

        return Response(
            {"detail": "Неверная почта или пароль"},
            status=status.HTTP_401_UNAUTHORIZED
        )

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)