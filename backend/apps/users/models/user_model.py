from config.abstact_models import BaseModelAbstract
from django.db import models


class User(BaseModelAbstract):
    """
    Модель пользователя.
    """

    email = models.EmailField('Email', unique=True)
    password_hash = models.CharField(
        'Хэш пароля',
        max_length=256,
    )

    first_name = models.CharField(
        'Имя',
        max_length=128,
        default='',
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=128,
        default='',
        blank=True,
    )
    patronymic = models.CharField(
        'Отчество',
        max_length=128,
        default='',
        blank=True,
    )

    is_active = models.BooleanField(
        'Активен',
        default=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
