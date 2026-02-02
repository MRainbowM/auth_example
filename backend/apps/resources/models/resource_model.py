from apps.users.models import User
from config.abstract_models import BaseModelAbstract
from django.db import models


class Resource(BaseModelAbstract):
    """
    Модель ресурса.
    """
    name = models.CharField(
        'Название ресурса',
        max_length=255,
        unique=True,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Владелец ресурса',
    )

    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'

    def __str__(self):
        return self.name
