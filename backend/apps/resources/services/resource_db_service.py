from typing import Optional
from uuid import UUID

from apps.resources.models import Resource
from config.abstact_classes.abstract_db_service import AbstractDBService
from django.db.models import Q


class ResourceDBService(AbstractDBService[Resource]):
    """
    Сервис для работы с ресурсами.
    """

    def __init__(self):
        self.model = Resource

    async def _get_filters(
            self,
            resource_id__in: Optional[list[UUID]] = None,
            owner_id: Optional[UUID] = None,
    ) -> Q:
        """
        Получение фильтров для ресурса.

        :param resource_id__in: Список ID ресурсов.
        :param owner_id: ID владельца ресурса.
        :return: Фильтры.
        """
        filters = Q()

        if resource_id__in:
            filters &= Q(id__in=resource_id__in)

        if owner_id:
            filters &= Q(owner_id=owner_id)

        return filters


resource_db_service = ResourceDBService()
