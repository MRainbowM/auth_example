from apps.authorization.constants import PERMISSIONS_LITERAL
from apps.resources.models import Resource
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
        roles = await role_db_service.get_roles_by_user(user=user)
        role_ids = [role.id for role in roles]

        # Поиск права доступа ресурса по ролям пользователя
        if await role_permission_db_service.exists_permission(
                role_ids=role_ids,
                resource_id=resource.id,
                permission=permission,
        ):
            # Существует право доступа к ресурсу
            return True

        # Нет доступа
        return False


authorization_service = AuthorizationService()
