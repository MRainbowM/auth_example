from __future__ import annotations

from typing import Any, Optional
from uuid import UUID

import jwt
from apps.authentication.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from apps.users.models import User
from config.settings import JWT_ALGORITHM, JWT_PUBLIC_KEY


async def jwt_auth(request) -> Optional[User]:
    """
    Асинхронная авторизация для Django Ninja через JWT в заголовке:
    Authorization: Bearer <token>

    При успехе возвращает пользователя (будет доступен как request.auth),
    при провале возвращает None (Ninja ответит 401).
    """
    auth_header = (
            request.headers.get("Authorization") or
            request.META.get("HTTP_AUTHORIZATION")
    )
    if not auth_header:
        return None

    # Ожидается "Bearer <token>"
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    token = parts[1]
    access_token_type = ACCESS_TOKEN_TYPE

    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            JWT_PUBLIC_KEY,
            algorithms=[JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        return None

    if payload.get("type") != access_token_type:
        return None

    sub = payload.get("sub")
    if not sub:
        return None

    try:
        user_id = UUID(str(sub))
    except ValueError:
        return None

    # Фильтруем пользователей по id и активности
    return await User.objects.filter(id=user_id, is_active=True).afirst()
