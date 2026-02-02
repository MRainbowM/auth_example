from typing import Optional
from uuid import UUID

from apps.resources.models import Resource


class ResourceDBService:
    """
    Сервис для работы с ресурсами.
    """

    def __init__(self):
        self.model = Resource

    async def get_resource_by_id(self, resource_id: UUID) -> Optional[Resource]:
        """
        Получение ресурса по id.

        :param resource_id: ID ресурса.
        :return: Ресурс.
        """
        return await self.model.objects.filter(id=resource_id).afirst()


resource_db_service = ResourceDBService()
