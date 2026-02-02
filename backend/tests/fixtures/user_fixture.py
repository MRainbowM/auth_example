import pytest
from apps.users.models import User
from apps.users.services.password_service import password_service


@pytest.fixture
async def user_fixture() -> User:
    """
    Фикстура для создания пользователя.
    """
    password_str = 'testpassword'
    hashed_password = await password_service.hash_password(
        password=password_str
    )
    user, _ = await User.objects.aget_or_create(
        email='test@test.com',
        defaults={
            'password_hash': hashed_password,
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'patronymic': 'Иванович',
        },
    )

    user.password_str = password_str
    return user


@pytest.fixture
async def user_owner_resource_fixture() -> User:
    """
    Фикстура для создания пользователя - владельца ресурса.
    """
    password_str = 'testpassword'
    hashed_password = await password_service.hash_password(
        password=password_str
    )
    user, _ = await User.objects.aget_or_create(
        email='owner@test.com',
        defaults={
            'password_hash': hashed_password,
        },
    )
    return user
