from uuid import UUID

from apps.authorization.models import RolePermission
from apps.users.models import User
from ninja.errors import HttpError

from .role_permission_db_service import role_permission_db_service
from ..schemas import PermissionUpdateSchema


class AuthorizationApiService:
    """
    Сервис для работы с API авторизации.
    """

    async def get_permissions(self, user: User):
        """
        Получение всех прав доступа.
        Метод доступен только админам системы.

        :param user: Пользователь.
        :return: Список прав доступа.
        :raises HttpError(403): Если пользователь не является администратором.
        """
        if user.is_admin is False:
            raise HttpError(
                status_code=403,
                message='Доступ запрещен.',
            )
        return await role_permission_db_service.get_all_permissions()

    async def update_permission(
            self,
            user: User,
            data: PermissionUpdateSchema,
            permission_id: UUID,
    ) -> RolePermission:
        """
        Обновление права доступа.
        Метод доступен только админам системы и владельцам ресурсов.

        :param user: Пользователь.
        :param data: Данные для обновления прав доступа.
        :param permission_id: ID права доступа.
        :return: Обновленное право доступа.
        :raises HttpError(403): Если пользователь не является администратором.
        :raises HttpError(404): Если права доступа не найдено.
        """

        permission = await role_permission_db_service.get_permission_by_id(permission_id=permission_id)
        if permission is None:
            raise HttpError(
                status_code=404,
                message='Право доступа не найдено.',
            )

        if user.is_admin is False and permission.resource.owner_id != user.id:
            raise HttpError(
                status_code=403,
                message='Доступ запрещен.',
            )

        return await role_permission_db_service.update_permission(
            permission_in_db=permission,
            read_permission=data.read_permission,
            read_all_permission=data.read_all_permission,
            create_permission=data.create_permission,
            update_permission=data.update_permission,
            update_all_permission=data.update_all_permission,
            delete_permission=data.delete_permission,
            delete_all_permission=data.delete_all_permission,
        )


authorization_api_service = AuthorizationApiService()
