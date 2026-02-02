from uuid import UUID

from apps.authorization.constants import READ_PERMISSION, READ_ALL_PERMISSION
from apps.authorization.services.authorization_service import authorization_service
from apps.resources.models import Resource
from apps.resources.services.resource_db_service import resource_db_service
from apps.users.models import User
from ninja.errors import HttpError


class ResourceAPIService:
    """
    Сервис для работы с ресурсами.
    """

    def __init__(self):
        self.resource_return_fields = ['id', 'name']

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
        resource = await resource_db_service.get_by_id(
            object_id=resource_id,
            return_fields=self.resource_return_fields + ['owner_id'],
        )
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

    async def get_all_resources(
            self,
            user: User,
    ) -> list[Resource]:
        """
        Получение списка всех доступных ресурсов пользователю.
        :param user: Пользователь.
        :return: Список ресурсов.
        """
        if user.is_admin:
            # Администратор может получить доступ к любому ресурсу
            return await resource_db_service.get_list(return_fields=self.resource_return_fields)

        resource_ids = await authorization_service.get_all_resources_by_user_role(
            user=user,
            permission=READ_ALL_PERMISSION,  # Право на чтение списка всех ресурсов
        )
        resources = await resource_db_service.get_list(
            resource_id__in=resource_ids,
            return_fields=self.resource_return_fields,
        )
        return resources


resource_api_service = ResourceAPIService()
