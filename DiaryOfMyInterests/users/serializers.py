from rest_framework import serializers
from .models import Users
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'email', 'username', 'date_joined']


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Хэшируем пароль при создании
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
