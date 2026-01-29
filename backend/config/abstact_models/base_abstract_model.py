import uuid6
from django.db import models


class BaseModelAbstract(models.Model):
    """
    Базовая абстрактная модель для всех моделей с общими полями.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid6.uuid6,
        editable=False,
        unique=True
    )

    # Даты создания, обновления
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        abstract = True
