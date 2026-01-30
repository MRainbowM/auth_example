from dataclasses import dataclass
from datetime import timedelta
from uuid import uuid4

import jwt
from apps.users.models import User
from config.settings import (
    JWT_ACCESS_TOKEN_LIFETIME,
    JWT_ALGORITHM,
    JWT_PRIVATE_KEY,
    JWT_REFRESH_TOKEN_LIFETIME,
)
from django.utils import timezone

from ..constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE


@dataclass
class AuthTokens:
    """
    Токены аутентификации.
    """
    access: str
    refresh: str


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

        access_payload = {
            'type': self.access_token_type,
            'jti': uuid4().hex,  # Уникальный идентификатор токена
            'sub': str(user.id),
            'email': user.email,
            'iat': int(now.timestamp()),  # Время создания токена
            'exp': int(access_expires_at.timestamp()),
        }

        refresh_payload = {
            'type': self.refresh_token_type,
            'jti': uuid4().hex,
            'sub': str(user.id),
            'email': user.email,
            'iat': int(now.timestamp()),
            'exp': int(refresh_expires_at.timestamp()),
        }

        access_token = jwt.encode(
            access_payload,
            self.jwt_private_key,
            algorithm=self.jwt_algorithm,
        )

        refresh_token = jwt.encode(
            refresh_payload,
            self.jwt_private_key,
            algorithm=self.jwt_algorithm,
        )

        return AuthTokens(
            access=access_token,
            refresh=refresh_token,
        )


jwt_service = JWTService()
