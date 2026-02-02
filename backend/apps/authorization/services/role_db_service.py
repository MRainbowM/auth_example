from typing import Optional
from uuid import UUID

from apps.authorization.models import Role
from apps.users.models import User


class RoleDBService:
    """
    Сервис для работы с ролями.
    """

    def __init__(self):
        self.model = Role

    async def get_roles_by_user(self, user: User) -> list[Role]:
        """
        Получение ролей пользователя.

        :param user: Пользователь.
        :return: Роли пользователя.
        """
        qs = self.model.objects.filter(user_roles__user=user).all()
        return [obj async for obj in qs]

    async def create_role(self, name: str) -> Role:
        """
        Создание роли.
        :param name: Название роли.
        :return: Созданная роль.
        """
        return await self.model.objects.acreate(name=name)

    async def get_roles(self) -> list[Role]:
        """
        Получение списка ролей.
        :return: Список ролей.
        """
        qs = self.model.objects.all()
        return [obj async for obj in qs]

    async def get_role_by_id(self, role_id: UUID) -> Optional[Role]:
        """
        Получение роли по id.
        :param role_id: ID роли.
        :return: Роль.
        """
        return await self.model.objects.filter(id=role_id).afirst()


role_db_service = RoleDBService()
