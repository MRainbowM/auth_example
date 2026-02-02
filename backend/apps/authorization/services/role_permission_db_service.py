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

    async def get_permission_by_id(self, id: UUID) -> Optional[RolePermission]:
        """
        Получение права доступа по id.

        :param id: ID права доступа.
        :return: Право доступа.
        """
        return await self.model.objects.filter(id=id).afirst()


role_permission_db_service = RolePermissionDBService()
