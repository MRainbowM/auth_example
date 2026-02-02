from typing import List
from typing import Optional
from uuid import UUID

from apps.authorization.constants import PERMISSIONS_LITERAL
from apps.authorization.models import RolePermission
from config.abstact_classes.abstract_db_service import AbstractDBService
from django.db.models import Q


class RolePermissionDBService(AbstractDBService[RolePermission]):
    """
    Сервис для работы с базой данных прав доступа.
    """

    def __init__(self):
        self.model = RolePermission

    async def _get_filters(
            self,
            **kwargs
    ) -> Q:
        """
        Получение фильтров для RolePermission.
        """
        filters = Q()
        return filters

    async def _get_select_related(
            self,
            join_role: Optional[bool] = None,
            join_resource: Optional[bool] = None,
            **kwargs
    ) -> List[str]:
        """
        Получение select_related для RolePermission.

        :param join_role: Объединять с ролью.
        :param join_resource: Объединять с ресурсом.
        :return: Список select_related.
        """
        select_related = []

        if join_role is True:
            select_related.append('role')

        if join_resource is True:
            select_related.append('resource')

        return select_related

    async def update_permission(
            self,
            permission_in_db: RolePermission,
            read_permission: bool,
            read_all_permission: bool,
            create_permission: bool,
            update_permission: bool,
            update_all_permission: bool,
            delete_permission: bool,
            delete_all_permission: bool,
    ) -> RolePermission:
        """
        Обновление права доступа.

        :param permission_in_db: Объект права доступа в базе данных.
        :param read_permission: Право на чтение.
        :param read_all_permission: Право на чтение всех объектов.
        :param create_permission: Право на создание.
        :param update_permission: Право на обновление.
        :param update_all_permission: Право на обновление всех объектов.
        :param delete_permission: Право на удаление.
        :param delete_all_permission: Право на удаление всех объектов.
        :return: Обновленное право доступа.
        """
        permission_in_db.read_permission = read_permission
        permission_in_db.read_all_permission = read_all_permission
        permission_in_db.create_permission = create_permission
        permission_in_db.update_permission = update_permission
        permission_in_db.update_all_permission = update_all_permission
        permission_in_db.delete_permission = delete_permission
        permission_in_db.delete_all_permission = delete_all_permission
        await permission_in_db.asave()
        return permission_in_db

    async def exists_permission(
            self,
            role_ids: list[UUID],
            resource_id: UUID,
            permission: PERMISSIONS_LITERAL,
    ) -> bool:
        """
        Проверка существования роли, имеющей права доступа к ресурсу.

        :param role_ids: Список ID ролей.
        :param resource_id: ID ресурса.
        :param permission: Право доступа.
        :return: True, если права доступа существуют, False в противном случае.
        """
        return await self.model.objects.filter(
            resource_id=resource_id,
            role_id__in=role_ids,
            **{permission: True},
        ).aexists()

    async def get_resources_by_roles(
            self,
            role_ids: list[UUID],
            permission: PERMISSIONS_LITERAL,
    ) -> list[UUID]:
        """
        Получение списка ID ресурсов, доступных для указанных ролей.

        :param role_ids: Список ID ролей.
        :param permission: Право доступа.
        :return: Список ID ресурсов.
        """
        if not role_ids:
            return []

        qs = (
            self.model.objects.filter(
                role_id__in=role_ids,
                **{permission: True},
            )
            .values_list('resource_id', flat=True)
            .distinct()
        )
        return [resource_id async for resource_id in qs]


role_permission_db_service = RolePermissionDBService()
