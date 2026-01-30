import pytest
from apps.users.models import User

from .conftest import async_client


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_login_user():
    """
    Тест входа в систему.
    """

    email = 'test@test.com'
    password = 'testpassword'

    # Удаление пользователя, если он существует.
    await User.objects.filter(email=email).adelete()

    # Регистрация пользователя.
    response = await async_client.post(
        '/v1/authentication/register/',
        json={
            'email': email,
            'password': password,
            'password_repeat': password,
        },
    )
    assert response.status_code == 200, (
        'Регистрация пользователя не прошла. '
        f'Статус: {response.status_code}. '
        f'Ответ: {response.json()}.'
    )

    # Вход в систему.
    response = await async_client.post(
        '/v1/authentication/login/',
        json={
            'email': email,
            'password': password,
        },
    )
    assert response.status_code == 200, (
        'Вход в систему не прошёл. '
        f'Статус: {response.status_code}. '
        f'Ответ: {response.json()}.'
    )

    auth_tokens = response.json()
    assert auth_tokens['access'] is not None
    assert auth_tokens['refresh'] is not None
