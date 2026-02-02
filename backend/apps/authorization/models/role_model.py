from config.abstact_models import BaseModelAbstract
from django.db import models


class Role(BaseModelAbstract):
    """
    Модель роли.
    """
    name = models.CharField(
        'Название роли',
        max_length=255,
        unique=True,
    )

    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'
