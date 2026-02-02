from typing import Optional

from apps.authentication.constants import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_LITERAL,
)
from apps.authentication.dataclasses import AuthData
from apps.authentication.dataclasses import AuthTokenPayload
from apps.authentication.services.jwt_service import jwt_service
from apps.authentication.services.token_blacklist_db_service import token_blacklist_db_service
from apps.users.models import User
from django.utils import timezone
from ninja.security import HttpBearer


class JWTAuth(HttpBearer):
    """
    Bearer-auth для Django Ninja:
    Authorization: Bearer <token>
    """

    def __init__(self, token_type: TOKEN_TYPE_LITERAL):
        self.token_type = token_type
        return super().__init__()

    async def check_token_type(self, token_data: AuthTokenPayload) -> bool:
        """
        Проверка типа токена.

        :param token_data: Данные токена.
        :return: True, если тип токена соответствует, False - если не соответствует.
        """
        if token_data.type != self.token_type:
            return False
        return True

    async def check_token_expired(self, token_data: AuthTokenPayload) -> bool:
        """
        Проверка срока действия токена.

        :param token_data: Данные токена.
        :return: True, если токен не истек, False - если истек.
        """
        now = timezone.now()

        if token_data.exp < int(now.timestamp()):
            return False
        return True

    async def authenticate(self, request, token: str) -> Optional[AuthData]:
        """
        Аутентификация пользователя по токену.

        :param request: Запрос.
        :param token: Токен.
        :return: AuthData.
        """

        token_data = await jwt_service.decode_token(token=token)
        if not token_data:
            return None

        if not await self.check_token_expired(token_data=token_data):
            return None

        if not await self.check_token_type(token_data=token_data):
            return None

        user = await User.objects.filter(
            id=token_data.sub,
            is_active=True,
        ).afirst()
        if not user:
            return None

        # Поиск токена в TokenBlacklist
        is_token_in_blacklist = await token_blacklist_db_service.exists(token_jti=token_data.jti)
        if is_token_in_blacklist:
            # Токен отозван
            return None

        return AuthData(user=user, token_data=token_data)


# Авторизация по access токену
jwt_auth = JWTAuth(token_type=ACCESS_TOKEN_TYPE)
# Авторизация по refresh токену
refresh_jwt_auth = JWTAuth(token_type=REFRESH_TOKEN_TYPE)
