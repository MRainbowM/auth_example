from typing import Optional
from uuid import UUID

from apps.authorization.models import RolePermission


class RolePermissionDBService:
    """
    Сервис для работы с базой данных прав доступа.
    """

    def __init__(self):
        self.model = RolePermission

    async def get_all_permissions(self) -> list[RolePermission]:
        """
        Получение всех прав доступа.
        """
        qs = self.model.objects.select_related('role', 'resource').all()
        return [obj async for obj in qs]

    async def get_permission_by_id(self, permission_id: UUID) -> Optional[RolePermission]:
        """
        Получение права доступа по id.

        :param permission_id: ID права доступа.
        :return: Право доступа.
        """
        return await self.model.objects.filter(id=permission_id).select_related('role', 'resource').afirst()

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


role_permission_db_service = RolePermissionDBService()
