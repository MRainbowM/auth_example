import pytest
from apps.authentication.models import TokenBlacklist
from apps.authentication.services.jwt_service import AuthTokens
from apps.authentication.services.jwt_service import jwt_service
from apps.users.models import User

from .conftest import async_client


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_users(
        user_fixture: User,
        auth_tokens_fixture: AuthTokens,
        user_owner_resource_fixture: User,
):
    """
    Тест получения списка пользователей.

    :param user_fixture: Фикстура пользователя, который инициирует запрос.
    :param auth_tokens_fixture: Фикстура токенов авторизации.
    :param user_owner_resource_fixture: Фикстура пользователя, который будет в списке пользователей.
    """
    # Установка роли администратора
    user_fixture.is_admin = True
    await user_fixture.asave()

    response = await async_client.get(
        '/v1/users/',
        headers={'Authorization': f'Bearer {auth_tokens_fixture.access}'},
    )
    assert response.status_code == 200, (
        'Получение списка пользователей не прошло. '
        f'Статус: {response.status_code}. '
        f'Ответ: {response.json()}.'
    )
    response_data = response.json()
    assert len(response_data) == 2

    for user in response_data:
        if user['id'] == str(user_owner_resource_fixture.id):
            assert user['email'] == user_owner_resource_fixture.email
            assert user['first_name'] == user_owner_resource_fixture.first_name
            assert user['last_name'] == user_owner_resource_fixture.last_name
            assert user['patronymic'] == user_owner_resource_fixture.patronymic
        else:
            assert user['email'] != user_owner_resource_fixture.email
            assert user['first_name'] != user_owner_resource_fixture.first_name
            assert user['last_name'] != user_owner_resource_fixture.last_name
            assert user['patronymic'] != user_owner_resource_fixture.patronymic


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_user(
        auth_tokens_fixture: AuthTokens,
        user_fixture: User,
):
    """
    Тест получения информации о текущем пользователе.
    """
    response = await async_client.get(
        '/v1/users/me/',
        headers={'Authorization': f'Bearer {auth_tokens_fixture.access}'},
    )
    assert response.status_code == 200, (
        'Получение информации о текущем пользователе не прошло. '
        f'Статус: {response.status_code}. '
        f'Ответ: {response.json()}.'
    )

    response_data = response.json()
    assert response_data['id'] == str(user_fixture.id)
    assert response_data['email'] == user_fixture.email
    assert response_data['first_name'] == user_fixture.first_name
    assert response_data['last_name'] == user_fixture.last_name
    assert response_data['patronymic'] == user_fixture.patronymic


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_update_user(
        auth_tokens_fixture: AuthTokens,
        user_fixture: User,
):
    """
    Тест обновления информации о текущем пользователе.
    """
    payload = {
        'first_name': 'Петр',
        'last_name': 'Петров',
        'patronymic': 'Петрович',
    }
    response = await async_client.patch(
        '/v1/users/me/',
        headers={'Authorization': f'Bearer {auth_tokens_fixture.access}'},
        json=payload,
    )

    assert response.status_code == 200, (
        'Обновление информации о текущем пользователе не прошло. '
        f'Статус: {response.status_code}. '
        f'Ответ: {response.json()}.'
    )

    response_data = response.json()
    assert response_data['id'] == str(user_fixture.id)
    assert response_data['email'] == user_fixture.email
    assert response_data['first_name'] == payload['first_name']
    assert response_data['last_name'] == payload['last_name']
    assert response_data['patronymic'] == payload['patronymic']


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_delete_user(
        auth_tokens_fixture: AuthTokens,
        user_fixture: User,
):
    """
    Тест удаления текущего пользователя.

    :param auth_tokens_fixture: Фикстура токенов.
    :param user_fixture: Фикстура пользователя.
    """
    # Удаление пользователя.
    response = await async_client.delete(
        '/v1/users/me/',
        headers={'Authorization': f'Bearer {auth_tokens_fixture.access}'},
    )
    assert response.status_code == 204, (
        'Удаление текущего пользователя не прошло. '
        f'Статус: {response.status_code}. '
        f'Ответ: {response.json()}.'
    )

    # Проверка, что пользователь не может залогиниться после удаления.
    response = await async_client.post(
        '/v1/authentication/login/',
        json={
            'email': user_fixture.email,
            'password': user_fixture.password_str,
        },
    )

    assert response.status_code == 401, (
        'Пользователь может залогиниться после удаления. '
        f'Статус: {response.status_code}. '
        f'Ответ: {response.json()}.'
    )

    # Проверка, что токен отозван
    token_data = await jwt_service.decode_token(token=auth_tokens_fixture.access)
    is_token_in_blacklist = await TokenBlacklist.objects.filter(token_jti=token_data.jti).aexists()
    assert is_token_in_blacklist, 'Токен не добавлен в TokenBlacklist.'
