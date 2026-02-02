from config.abstact_models import BaseModelAbstract
from django.db import models

from ..models import Role, Resource


class RolePermission(BaseModelAbstract):
    """
    Модель правил доступа роли к ресурсу.
    """
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name='Роль',
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        verbose_name='Ресурс',
    )
    read_permission = models.BooleanField(
        'Право на чтение',
        default=False,
    )
    read_all_permission = models.BooleanField(
        'Право на чтение списка всех объектов',
        default=False,
    )
    create_permission = models.BooleanField(
        'Право на создание',
        default=False,
    )
    update_permission = models.BooleanField(
        'Право на обновление',
        default=False,
    )
    update_all_permission = models.BooleanField(
        'Право на обновление всех объектов',
        default=False,
    )
    delete_permission = models.BooleanField(
        'Право на удаление',
        default=False,
    )
    delete_all_permission = models.BooleanField(
        'Право на удаление всех объектов',
        default=False,
    )

    class Meta:
        verbose_name = 'Право доступа роли к ресурсу'
        verbose_name_plural = 'Права доступа ролей к ресурсам'

        # Уникальность сочетания роли и ресурса.
        unique_together = ('role', 'resource')
