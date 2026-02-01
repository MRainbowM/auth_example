from datetime import timedelta
from typing import Optional
from uuid import uuid4

import jwt
from apps.users.models import User
from config.settings import (
    JWT_ACCESS_TOKEN_LIFETIME,
    JWT_ALGORITHM,
    JWT_PRIVATE_KEY,
    JWT_REFRESH_TOKEN_LIFETIME,
    JWT_PUBLIC_KEY,
)
from django.utils import timezone

from ..constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from ..dataclasses import AuthTokenPayload, AuthTokens


class JWTService:
    """
    Сервис для работы с JWT токенами.
    """

    def __init__(self):
        self.jwt_access_token_lifetime = JWT_ACCESS_TOKEN_LIFETIME
        self.jwt_access_token_lifetime_delta = timedelta(
            seconds=self.jwt_access_token_lifetime
        )
        self.jwt_refresh_token_lifetime = JWT_REFRESH_TOKEN_LIFETIME
        self.jwt_refresh_token_lifetime_delta = timedelta(
            seconds=self.jwt_refresh_token_lifetime
        )

        self.jwt_algorithm = JWT_ALGORITHM
        self.jwt_private_key = JWT_PRIVATE_KEY
        self.jwt_public_key = JWT_PUBLIC_KEY

        self.access_token_type = ACCESS_TOKEN_TYPE
        self.refresh_token_type = REFRESH_TOKEN_TYPE

    async def create_auth_tokens(self, user: User) -> AuthTokens:
        """
        Создание токенов аутентификации.

        :param user: Пользователь.
        :return: Токены аутентификации.
        """
        now = timezone.now()
        access_expires_at = now + self.jwt_access_token_lifetime_delta
        refresh_expires_at = now + self.jwt_refresh_token_lifetime_delta

        access_payload = AuthTokenPayload(
            type=self.access_token_type,
            jti=uuid4().hex,  # Уникальный идентификатор токена
            sub=user.id,
            email=user.email,
            iat=int(now.timestamp()),  # Время создания токена
            exp=int(access_expires_at.timestamp()),
        )

        refresh_payload = AuthTokenPayload(
            type=self.refresh_token_type,
            jti=uuid4().hex,
            sub=user.id,
            email=user.email,
            iat=int(now.timestamp()),
            exp=int(refresh_expires_at.timestamp()),
        )

        access_token = jwt.encode(
            access_payload.to_dict(),
            self.jwt_private_key,
            algorithm=self.jwt_algorithm,
        )

        refresh_token = jwt.encode(
            refresh_payload.to_dict(),
            self.jwt_private_key,
            algorithm=self.jwt_algorithm,
        )

        return AuthTokens(
            access=access_token,
            refresh=refresh_token,
        )

    async def decode_token(self, token: str) -> Optional[AuthTokenPayload]:
        """
        Декодирование токена.
        Если токен невалидный, возвращает None.

        :param token: Токен.
        :return: Payload токена.
        """
        try:
            payload = jwt.decode(
                token,
                self.jwt_public_key,
                algorithms=[self.jwt_algorithm]
            )

        except jwt.PyJWTError:
            return None

        try:
            return AuthTokenPayload(**payload)
        except TypeError:
            return None


jwt_service = JWTService()
