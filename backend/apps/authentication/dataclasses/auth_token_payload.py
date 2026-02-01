from dataclasses import dataclass
from uuid import UUID

from ..constants import TOKEN_TYPE_LITERAL


@dataclass
class AuthTokenPayload:
    """
    Payload токена аутентификации.
    """
    type: TOKEN_TYPE_LITERAL
    jti: str
    sub: UUID
    email: str
    iat: int
    exp: int

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "jti": self.jti,
            "sub": str(self.sub),
            "email": self.email,
            "iat": self.iat,
            "exp": self.exp,
        }
