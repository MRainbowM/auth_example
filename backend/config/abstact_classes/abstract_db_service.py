from abc import ABC
from typing import Generic, List, Optional, Type, TypeVar, Union
from uuid import UUID

from django.db import models
from django.db.models import Q, QuerySet

ModelType = TypeVar('ModelType', bound=models.Model)


class AbstractDBService(ABC, Generic[ModelType]):
    """
    Абстрактный сервис для работы с Django-моделями.
    """

    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model

    async def _get_filters(self, **kwargs) -> Q:
        """
        Абстрактный метод для получения QuerySet фильтров.
        Должен быть переопределен в дочернем классе.
        """
        filters = Q()
        return filters

    async def _get_select_related(self, **kwargs) -> List[str]:
        """
        Абстрактный метод для получения таблиц, 1-m, которые можно заджойнить.
        :return: Возвращает список строковых названий таблиц.
        """
        return []

    async def _get_prefetch_related(self, **kwargs) -> List[str]:
        """
        Абстрактный метод для получения prefetch_related, таблиц m-m.
        """
        return []

    async def _exclude(self, queryset: QuerySet[ModelType], **kwargs) -> QuerySet:
        """
        Абстрактный метод, который исключает строки по значение параметров.
        """
        return queryset

    async def _filter_queryset(
            self,
            return_fields: Optional[List[str]] = None,
            order_by: Union[List[str], str] = None,
            **kwargs,
    ) -> QuerySet[ModelType]:
        """
        Возвращает отфильтрованный QuerySet.
        """
        if return_fields is None:
            return_fields = ['id']

        filters = await self._get_filters(**kwargs)

        # Фильтрация
        queryset = self.model.objects.filter(filters)

        # Исключения
        queryset = await self._exclude(queryset=queryset, **kwargs)

        # Присоединение таблиц
        select_related_array = await self._get_select_related(**kwargs)
        if select_related_array:
            queryset = queryset.select_related(*select_related_array)

        prefetch_related_array = await self._get_prefetch_related(**kwargs)
        if prefetch_related_array:
            queryset = queryset.prefetch_related(*prefetch_related_array)

        # Сортировка
        if order_by is not None:
            if isinstance(order_by, str):
                order_by = [order_by]
            queryset = queryset.order_by(*order_by)

        # Получение только запрашиваемых полей
        queryset = queryset.only(*return_fields)

        return queryset

    async def get_by_id(self, object_id: UUID, **kwargs) -> Optional[ModelType]:
        """
        Получение объекта по ID с применением фильтров.
        """

        queryset = await self._filter_queryset(**kwargs)
        return await queryset.filter(id=object_id).afirst()

    async def exists(self, **kwargs) -> bool:
        """
        Проверяет, существует ли объект по фильтрам.
        """
        queryset = await self._filter_queryset(**kwargs)
        return await queryset.aexists()

    async def get_list(self, **kwargs) -> List[ModelType]:
        """
        Получает список объектов.
        """
        queryset = await self._filter_queryset(**kwargs)
        queryset = queryset.distinct()  # Убрать дубликаты
        return [obj async for obj in queryset]

    async def get_first(self, **kwargs) -> Optional[ModelType]:
        """
        Возвращает первый объект после фильтрации.
        """
        queryset = await self._filter_queryset(**kwargs)
        return await queryset.afirst()
