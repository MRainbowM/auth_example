import pytest
from apps.users.models import User

from .conftest import async_client


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_register_user():
    """
    Тест регистрации пользователя.
    """
    # Удаление пользователя, если он существует.
    await User.objects.filter(email='test@test.com').adelete()

    response = await async_client.post(
        '/v1/authentication/register/',
        json={
            'email': 'test@test.com',
            'password': 'testpassword',
            'password_repeat': 'testpassword',
        },
    )
    assert response.status_code == 200, (
        'Регистрация пользователя не прошла. '
        f'Статус: {response.status_code}. '
        f'Ответ: {response.json()}.'
    )
