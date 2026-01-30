import pytest
from apps.authentication.services.jwt_service import AuthTokens
from apps.users.models import User

from .conftest import async_client


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
