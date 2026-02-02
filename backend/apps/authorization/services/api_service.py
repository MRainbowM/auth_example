from apps.users.models import User
from ninja.errors import HttpError

from .role_permission_db_service import role_permission_db_service


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
        """
        if user.is_admin is False:
            raise HttpError(
                status_code=403,
                message='Доступ запрещен.',
            )
        return await role_permission_db_service.get_all_permissions()


authorization_api_service = AuthorizationApiService()
