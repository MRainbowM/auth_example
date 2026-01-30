import pytest
from apps.users.models import User


@pytest.fixture
async def user_fixture() -> User:
    """
    Фикстура для создания пользователя.
    """
    user, _ = await User.objects.aget_or_create(
        email='test@test.com',
        defaults={
            'password': 'testpassword',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'patronymic': 'Иванович',
        },
    )
    return user
