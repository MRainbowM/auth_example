from datetime import timedelta

import jwt
from apps.users.models import User
from config.settings import JWT_ACCESS_TOKEN_LIFETIME, JWT_ALGORITHM, JWT_SECRET_KEY
from django.utils import timezone


class JWTService:
    def __init__(self):
        self.jwt_access_token_lifetime = JWT_ACCESS_TOKEN_LIFETIME
        self.jwt_algorithm = JWT_ALGORITHM
        self.jwt_secret_key = JWT_SECRET_KEY

    async def create_access_token(self, user: User) -> str:
        """
        Создание access токена.
        """

        now = timezone.now()
        expires_at = now + timedelta(seconds=self.jwt_access_token_lifetime)

        payload = {
            'sub': user.id,
            'email': user.email,
            'iat': int(now.timestamp()),
            'exp': int(expires_at.timestamp()),
        }

        token = jwt.encode(
            payload,
            self.jwt_secret_key,
            algorithm=self.jwt_algorithm,
        )

        return token
