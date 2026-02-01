from ..models import TokenBlacklist


class TokenBlacklistDBService:
    def __init__(self):
        self.model = TokenBlacklist

    async def add_token_to_blacklist(self, token_jti: str) -> None:
        """
        Добавление токена в черный список.

        :param token_jti: JTI токена - уникальный идентификатор токена.
        :return: None.
        """
        await self.model.objects.acreate(token_jti=token_jti)


token_blacklist_db_service = TokenBlacklistDBService()
