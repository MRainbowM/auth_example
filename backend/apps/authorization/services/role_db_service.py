from typing import Optional
from uuid import UUID

from apps.authorization.models import Role
from config.abstact_classes.abstract_db_service import AbstractDBService
from django.db.models import Q


class RoleDBService(AbstractDBService[Role]):
    """
    Сервис для работы с ролями.
    """

    def __init__(self):
        self.model = Role

    async def _get_filters(
            self,
            user_id: Optional[UUID] = None,
            **kwargs
    ) -> Q:
        """
        Получение фильтров для роли.

        :param user_id: ID пользователя.
        :return: Фильтры.
        """
        filters = Q()

        if user_id:
            filters &= Q(user_roles__user_id=user_id)

        return filters

    async def create_role(self, name: str) -> Role:
        """
        Создание роли.
        :param name: Название роли.
        :return: Созданная роль.
        """
        return await self.model.objects.acreate(name=name)


role_db_service = RoleDBService()
