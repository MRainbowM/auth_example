from uuid import UUID

from apps.authorization.constants import PERMISSIONS_LITERAL
from apps.resources.models import Resource
from apps.resources.services.resource_db_service import resource_db_service
from apps.users.models import User

from .role_db_service import role_db_service
from .role_permission_db_service import role_permission_db_service


class AuthorizationService:
    """
    Сервис для работы с правами доступа.
    """

    async def check_access(
            self,
            user: User,
            resource: Resource,
            permission: PERMISSIONS_LITERAL,
    ) -> bool:
        """
        Проверка прав доступа пользователя к ресурсу.

        :param user: Пользователь.
        :param resource: Ресурс.
        :param permission: Право доступа.
        :return: True, если есть доступ, False в противном случае.
        """
        # Проверка владения ресурсом пользователем
        if resource.owner_id == user.id:
            # Пользователь - владелец, может просматривать ресурс
            return True

        # Получение списка ID ролей пользователя
        roles = await role_db_service.get_list(user_id=user.id)
        role_ids = [role.id for role in roles]

        if len(role_ids) == 0:
            # Пользователь не имеет ролей
            return False

        # Поиск права доступа ресурса по ролям пользователя
        if await role_permission_db_service.exists(
                role_id__in=role_ids,
                resource_id=resource.id,
                permission=permission,
        ):
            # Существует право доступа к ресурсу
            return True

        # Нет доступа
        return False

    async def get_all_resources_by_user_role(
            self,
            user: User,
            permission: PERMISSIONS_LITERAL,
    ) -> list[UUID]:
        """
        Получение списка всех доступных ресурсов пользователю с указанным правом доступа.
        Или где пользователь является владельцем ресурса.

        :param user: Пользователь.
        :param permission: Право доступа.
        :return: Список ресурсов.
        """
        # Получение списка ресурсов, где пользователь является владельцем
        resources = await resource_db_service.get_list(owner_id=user.id)
        resource_ids = [resource.id for resource in resources]

        # Получение списка ролей пользователя
        roles = await role_db_service.get_list(user_id=user.id)
        role_ids = [role.id for role in roles]

        # Получение списка ресурсов, доступных пользователю по ролям
        resources_by_role = []

        if len(role_ids) > 0:
            role_permissions = await role_permission_db_service.get_list(
                role_id__in=role_ids,
                permission=permission,
                join_resource=True,
                return_fields=['resource_id'],
            )
            resources_by_role = [row.resource_id for row in role_permissions]

        return set(resource_ids + resources_by_role)


authorization_service = AuthorizationService()
