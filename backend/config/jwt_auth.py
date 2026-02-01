from typing import Optional

from apps.authentication.constants import ACCESS_TOKEN_TYPE
from apps.authentication.dataclasses import AuthData
from apps.authentication.models import TokenBlacklist
from apps.authentication.services.jwt_service import jwt_service
from apps.users.models import User
from ninja.security import HttpBearer


class JWTAuth(HttpBearer):
    """
    Bearer-auth для Django Ninja:
    Authorization: Bearer <token>
    """

    async def authenticate(self, request, token: str) -> Optional[AuthData]:
        """
        Аутентификация пользователя по токену.

        :param request: Запрос.
        :param token: Токен.
        :return: AuthData.
        """

        token_data = await jwt_service.decode_token(token)
        if not token_data:
            return None

        if token_data.type != ACCESS_TOKEN_TYPE:
            return None

        user = await User.objects.filter(
            id=token_data.sub,
            is_active=True,
        ).afirst()
        if not user:
            return None

        # Поиск токена в TokenBlacklist
        is_token_in_blacklist = await TokenBlacklist.objects.filter(token_jti=token_data.jti).aexists()
        if is_token_in_blacklist:
            # Токен отозван
            return None

        return AuthData(user=user, token_data=token_data)


jwt_auth = JWTAuth()
