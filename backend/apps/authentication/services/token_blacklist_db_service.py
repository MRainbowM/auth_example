from typing import Optional

from config.abstract_classes.abstract_db_service import AbstractDBService
from django.db.models import Q

from ..models import TokenBlacklist


class TokenBlacklistDBService(AbstractDBService[TokenBlacklist]):
    def __init__(self):
        self.model = TokenBlacklist

    async def _get_filters(
            self,
            token_jti: Optional[str] = None,
            **kwargs
    ) -> Q:
        """
        Получение фильтров для TokenBlacklist.

        :param token_jti: JTI токена.
        :return: Фильтры.
        """
        filters = Q()

        if token_jti:
            filters &= Q(token_jti=token_jti)

        return filters

    async def add_token_to_blacklist(self, token_jti: str) -> None:
        """
        Добавление токена в черный список.

        :param token_jti: JTI токена - уникальный идентификатор токена.
        :return: None.
        """
        await self.model.objects.acreate(token_jti=token_jti)


token_blacklist_db_service = TokenBlacklistDBService()
