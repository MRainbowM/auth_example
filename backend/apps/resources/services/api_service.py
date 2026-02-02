from uuid import UUID

from apps.authorization.constants import READ_PERMISSION
from apps.authorization.services.authorization_service import authorization_service
from apps.resources.models import Resource
from apps.resources.services.resource_db_service import resource_db_service
from apps.users.models import User
from ninja.errors import HttpError


class ResourceAPIService:
    """
    Сервис для работы с ресурсами.
    """

    async def get_resource_by_id(
            self,
            resource_id: UUID,
            user: User,
    ) -> Resource:
        """
        Получение ресурса по id.

        :param resource_id: ID ресурса.
        :param user: Пользователь.
        :return: Ресурс.
        """
        resource = await resource_db_service.get_resource_by_id(resource_id=resource_id)
        if resource is None:
            raise HttpError(
                status_code=404,
                message='Ресурс не найден.',
            )

        # Проверка доступа пользователя к ресурсу
        is_access = await authorization_service.check_access(
            user=user,
            resource=resource,
            permission=READ_PERMISSION,  # Право на чтение ресурса
        )
        if not is_access:
            raise HttpError(
                status_code=403,
                message='Нет доступа.',
            )
        return resource


resource_api_service = ResourceAPIService()
