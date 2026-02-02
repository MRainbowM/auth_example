from config.abstract_models import BaseModelAbstract
from django.db import models


class TokenBlacklist(BaseModelAbstract):
    """
    Модель токенов, которые были отозваны.
    """
    token_jti = models.CharField(
        'JTI токена',
        max_length=64,
        unique=True,
    )

    class Meta:
        verbose_name = 'Черный список токенов'
        verbose_name_plural = 'Черные списки токенов'
