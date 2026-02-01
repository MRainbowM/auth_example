from dataclasses import dataclass


@dataclass
class AuthTokens:
    """
    Токены аутентификации.
    """
    access: str
    refresh: str
