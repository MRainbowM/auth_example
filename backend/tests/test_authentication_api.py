import pytest
from apps.authentication.models import TokenBlacklist
from apps.authentication.services.jwt_service import AuthTokens
from apps.authentication.services.jwt_service import jwt_service
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


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_login_user(
        user_fixture: User,
):
    """
    Тест входа в систему.

    :param user_fixture: Фикстура пользователя.
    """

    # Вход в систему.
    response = await async_client.post(
        '/v1/authentication/login/',
        json={
            'email': user_fixture.email,
            'password': user_fixture.password_str,
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


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_logout_user(
        auth_tokens_fixture: AuthTokens,
):
    """
    Тест выхода из системы.

    :param auth_tokens_fixture: Фикстура токенов.
    """
    response = await async_client.post(
        '/v1/authentication/logout/',
        headers={'Authorization': f'Bearer {auth_tokens_fixture.access}'},
    )
    assert response.status_code == 204, (
        'Выход из системы не прошёл. '
        f'Статус: {response.status_code}. '
        f'Ответ: {response.json()}.'
    )

    token_data = await jwt_service.decode_token(token=auth_tokens_fixture.access)
    is_token_in_blacklist = await TokenBlacklist.objects.filter(token_jti=token_data.jti).aexists()
    assert is_token_in_blacklist, 'Токен не добавлен в TokenBlacklist.'

    # Проверка, что токен не может быть использован повторно
    response = await async_client.post(
        '/v1/authentication/logout/',
        headers={'Authorization': f'Bearer {auth_tokens_fixture.access}'},
    )
    assert response.status_code == 401, (
        'Токен может быть использован повторно. '
        f'Статус: {response.status_code}. '
        f'Ответ: {response.json()}.'
    )


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_refresh_token(
        auth_tokens_fixture: AuthTokens,
):
    """
    Тест обновления токена.

    :param auth_tokens_fixture: Фикстура токенов.
    """
    response = await async_client.post(
        '/v1/authentication/refresh/',
        headers={'Authorization': f'Bearer {auth_tokens_fixture.refresh}'},
    )
    assert response.status_code == 200, (
        'Обновление токена не прошло. '
        f'Статус: {response.status_code}. '
        f'Ответ: {response.json()}.'
    )

    auth_tokens = response.json()
    assert auth_tokens['access'] != auth_tokens_fixture.access is not None
    assert auth_tokens['refresh'] != auth_tokens_fixture.refresh is not None


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_refresh_token_invalid_token(
        auth_tokens_fixture: AuthTokens,
):
    """
    Тест обновления токена с неверным типом токена.

    :param auth_tokens_fixture: Фикстура токенов.
    """
    response = await async_client.post(
        '/v1/authentication/refresh/',
        headers={'Authorization': f'Bearer {auth_tokens_fixture.access}'},
    )
    assert response.status_code == 401, (
        'Неверный ответ от сервера. '
        f'Статус: {response.status_code}. '
        f'Ответ: {response.json()}.'
    )
