from typing import List, Optional

from apps.authorization.models import UserRole, Role
from apps.users.models import User
from config.abstact_classes.abstract_db_service import AbstractDBService


class UserRoleDBService(AbstractDBService[UserRole]):
    def __init__(self):
        self.model = UserRole

    async def _get_select_related(
            self,
            join_user: Optional[bool] = None,
            join_role: Optional[bool] = None,
            **kwargs
    ) -> List[str]:
        """
        Получение select_related для UserRole.

        :param join_user: Объединять с пользователем.
        :param join_role: Объединять с ролью.
        :return: Список select_related.
        """
        select_related = []

        if join_user is True:
            select_related.append('user')

        if join_role is True:
            select_related.append('role')

        return select_related

    async def create_user_role(self, user: User, role: Role) -> UserRole:
        """
        Назначение роли пользователю.

        :param user: Пользователь.
        :param role: Роль.
        :return: Назначенная роль.
        """
        user_role, _ = await self.model.objects.aget_or_create(user=user, role=role)
        return user_role


user_role_db_service = UserRoleDBService()
