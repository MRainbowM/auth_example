from dataclasses import dataclass

from apps.users.models import User

from .auth_token_payload import AuthTokenPayload


@dataclass
class AuthData:
    user: User
    token_data: AuthTokenPayload
