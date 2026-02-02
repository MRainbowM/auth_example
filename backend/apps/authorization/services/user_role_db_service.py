from uuid import UUID

from apps.authorization.models import UserRole, Role
from apps.users.models import User


class UserRoleDBService:
    def __init__(self):
        self.model = UserRole

    async def create_user_role(self, user: User, role: Role) -> UserRole:
        """
        Назначение роли пользователю.

        :param user: Пользователь.
        :param role: Роль.
        :return: Назначенная роль.
        """
        user_role, _ = await self.model.objects.aget_or_create(user=user, role=role)
        return user_role

    async def get_user_role_by_id(self, user_role_id: UUID) -> UserRole:
        """
        Получение связи пользователь↔роль по id.
        :param user_role_id: ID связи пользователь↔роль.
        :return: Связь пользователь↔роль.
        """
        return await self.model.objects.filter(id=user_role_id).select_related('user', 'role').afirst()


user_role_db_service = UserRoleDBService()
