import pytest
from apps.authentication.services.jwt_service import jwt_service, AuthTokens
from apps.users.models import User


@pytest.fixture
async def auth_tokens_fixture(
        user_fixture: User
) -> AuthTokens:
    """
    Фикстура для создания токенов аутентификации.
    """
    return await jwt_service.create_auth_tokens(user_fixture)
