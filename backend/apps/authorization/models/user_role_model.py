from apps.authorization.models import Role
from apps.users.models import User
from config.abstract_models import BaseModelAbstract
from django.db import models


class UserRole(BaseModelAbstract):
    """
    Модель связи пользователя и роли.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_roles',
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name='Роль',
        related_name='user_roles',
    )

    class Meta:
        verbose_name = 'Связь пользователя и роли'
        verbose_name_plural = 'Связи пользователя и роли'

        unique_together = ('user', 'role')
