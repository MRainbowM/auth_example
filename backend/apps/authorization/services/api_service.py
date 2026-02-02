from uuid import UUID

from apps.authorization.models import Role, RolePermission, UserRole
from apps.users.models import User
from apps.users.services.user_db_service import user_db_service
from ninja.errors import HttpError

from .role_db_service import role_db_service
from .role_permission_db_service import role_permission_db_service
from .user_role_db_service import user_role_db_service
from ..schemas import PermissionUpdateSchema
from ..schemas import RoleCreateSchema, UserRoleCreateSchema


class AuthorizationApiService:
    """
    Сервис для работы с API авторизации.
    """

    async def create_role(
            self,
            user: User,
            data: RoleCreateSchema
    ) -> Role:
        """
        Создание роли.
        Метод доступен только админам системы.

        :param user: Пользователь.
        :param data: Данные для создания роли.
        :return: Созданная роль.
        """
        if user.is_admin is False:
            raise HttpError(
                status_code=403,
                message='Доступ запрещен.',
            )
        return await role_db_service.create_role(name=data.name)

    async def get_roles(self, user: User) -> list[Role]:
        """
        Получение списка ролей.
        Метод доступен только админам системы.

        :param user: Пользователь.
        :return: Список ролей.
        :raises HttpError(403): Если пользователь не является администратором.
        """
        if user.is_admin is False:
            raise HttpError(
                status_code=403,
                message='Доступ запрещен.',
            )
        return await role_db_service.get_roles()

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

    async def create_user_role(self, user: User, data: UserRoleCreateSchema) -> UserRole:
        """
        Назначение роли пользователю.
        Метод доступен только админам системы.

        :param user: Пользователь.
        :param data: Данные для назначения роли пользователю.
        :return: Назначенная роль.
        :raises HttpError(403): Если пользователь не является администратором.
        :raises HttpError(404): Если роль или пользователь не найдены.
        """

        if user.is_admin is False:
            raise HttpError(
                status_code=403,
                message='Доступ запрещен.',
            )

        role = await role_db_service.get_role_by_id(role_id=data.role_id)
        if role is None:
            raise HttpError(
                status_code=404,
                message='Роль не найдена.',
            )

        user = await user_db_service.get_user_by_id(user_id=data.user_id)
        if user is None:
            raise HttpError(
                status_code=404,
                message='Пользователь не найден.',
            )

        user_role = await user_role_db_service.create_user_role(user=user, role=role)
        # Получение связи пользователь-роль после создания для возврата в API
        return await user_role_db_service.get_user_role_by_id(user_role_id=user_role.id)


authorization_api_service = AuthorizationApiService()
