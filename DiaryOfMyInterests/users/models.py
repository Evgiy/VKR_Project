from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):
    email = models.EmailField('Почта', unique=True, default='Почта')
    favorite_categories = models.JSONField(default=list, blank=True)
    favorite_tags = models.ManyToManyField('main.Tag', blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
