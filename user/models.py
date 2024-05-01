from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        permissions = [
            ("set_is_active", "Активация пользователя"),
            ("block_user", "Can block users"),
        ]

    email = models.EmailField(unique=True, verbose_name='Почта')
    username = models.CharField(max_length=150, unique=True, verbose_name='Имя пользователя')

    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='Страна', **NULLABLE)

    is_verified = models.BooleanField(default=False, verbose_name='Верификация')
    verification_code = models.CharField(max_length=100, verbose_name='Код верификации', **NULLABLE)

    have_permissions = models.BooleanField(default=False, verbose_name='Права доступа')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
