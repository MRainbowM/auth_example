import pytest
from apps.authorization.models import Role


@pytest.fixture
async def role_fixture() -> Role:
    """
    Фикстура для создания роли.

    :return: Созданная роль.
    """
    role, _ = await Role.objects.aget_or_create(
        name='Менеджер',
    )
    return role
