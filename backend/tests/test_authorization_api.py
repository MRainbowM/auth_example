import pytest
from apps.authentication.services.jwt_service import AuthTokens
from apps.authorization.models.role_permission_model import RolePermission
from apps.users.models import User

from .conftest import async_client


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_permissions(
        user_fixture: User,
        auth_tokens_fixture: AuthTokens,
        role_permission_fixture: RolePermission,
):
    """
    Тест получения списка прав доступа.

    :param user_fixture: Фикстура пользователя.
    :param auth_tokens_fixture: Фикстура токенов авторизации.
    :param role_permission_fixture: Фикстура права доступа.
    """
    # Установка роли администратора
    user_fixture.is_admin = True
    await user_fixture.asave()

    response = await async_client.get(
        '/v1/authorization/permissions/',
        headers={
            'Authorization': f'Bearer {auth_tokens_fixture.access}',
        },
    )

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]['id'] == str(role_permission_fixture.id)
    assert response_data[0]['role']['id'] == str(
        role_permission_fixture.role.id)
    assert response_data[0]['role']['name'] == role_permission_fixture.role.name
    assert response_data[0]['resource']['id'] == str(
        role_permission_fixture.resource.id)
    assert response_data[0]['resource']['name'] == role_permission_fixture.resource.name
    assert response_data[0]['read_permission'] == role_permission_fixture.read_permission
    assert response_data[0]['read_all_permission'] == role_permission_fixture.read_all_permission
    assert response_data[0]['create_permission'] == role_permission_fixture.create_permission
    assert response_data[0]['update_permission'] == role_permission_fixture.update_permission
    assert response_data[0]['update_all_permission'] == role_permission_fixture.update_all_permission
    assert response_data[0]['delete_permission'] == role_permission_fixture.delete_permission
    assert response_data[0]['delete_all_permission'] == role_permission_fixture.delete_all_permission


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_permissions_not_admin(
        user_fixture: User,
        auth_tokens_fixture: AuthTokens,
):
    """
    Тест получения списка прав доступа не администратором.
    Должен возвращаться статус 403.

    :param user_fixture: Фикстура пользователя.
    :param auth_tokens_fixture: Фикстура токенов авторизации.
    """
    # Установка роли не администратора
    user_fixture.is_admin = False
    await user_fixture.asave()

    response = await async_client.get(
        '/v1/authorization/permissions/',
        headers={
            'Authorization': f'Bearer {auth_tokens_fixture.access}',
        },
    )
    assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_update_permission(
        user_fixture: User,
        auth_tokens_fixture: AuthTokens,
        role_permission_fixture: RolePermission,
):
    """
    Тест обновления права доступа.

    :param user_fixture: Фикстура пользователя.
    :param auth_tokens_fixture: Фикстура токенов авторизации.
    :param role_permission_fixture: Фикстура права доступа к ресурсу.
    """

    # Установка роли администратора
    user_fixture.is_admin = True
    await user_fixture.asave()

    payload = {
        'read_permission': False,
        'read_all_permission': False,
        'create_permission': False,
        'update_permission': False,
        'update_all_permission': False,
        'delete_permission': False,
        'delete_all_permission': False,
    }
    response = await async_client.patch(
        f'/v1/authorization/permissions/{role_permission_fixture.id}/',
        json=payload,
        headers={
            'Authorization': f'Bearer {auth_tokens_fixture.access}',
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == str(role_permission_fixture.id)
    assert response_data['role']['id'] == str(
        role_permission_fixture.role_id
    )
    assert response_data['resource']['id'] == str(
        role_permission_fixture.resource_id
    )

    assert response_data['read_permission'] == payload['read_permission']
    assert response_data['read_all_permission'] == payload['read_all_permission']
    assert response_data['create_permission'] == payload['create_permission']
    assert response_data['update_permission'] == payload['update_permission']
    assert response_data['update_all_permission'] == payload['update_all_permission']
    assert response_data['delete_permission'] == payload['delete_permission']
    assert response_data['delete_all_permission'] == payload['delete_all_permission']


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_update_permission_not_admin(
        user_fixture: User,
        auth_tokens_fixture: AuthTokens,
        role_permission_fixture: RolePermission,
):
    """
    Тест обновления права доступа не администратором.
    Должен возвращаться статус 403.

    :param user_fixture: Фикстура пользователя.
    :param auth_tokens_fixture: Фикстура токенов авторизации.
    :param role_permission_fixture: Фикстура права доступа к ресурсу.
    """

    # Сброс роли администратора
    user_fixture.is_admin = False
    await user_fixture.asave()

    payload = {
        'read_permission': False,
        'read_all_permission': False,
        'create_permission': False,
        'update_permission': False,
        'update_all_permission': False,
        'delete_permission': False,
        'delete_all_permission': False,
    }
    response = await async_client.patch(
        f'/v1/authorization/permissions/{role_permission_fixture.id}/',
        json=payload,
        headers={
            'Authorization': f'Bearer {auth_tokens_fixture.access}',
        },
    )
    assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_update_permission_owner_resource(
        user_owner_resource_fixture: User,
        auth_tokens_owner_fixture: AuthTokens,
        role_permission_fixture: RolePermission,
):
    """
    Тест обновления права доступа владельцем ресурса, но не администратором.


    :param user_owner_resource_fixture: Фикстура пользователя - владельца ресурса.
    :param auth_tokens_fixture: Фикстура токенов авторизации.
    :param role_permission_fixture: Фикстура права доступа к ресурсу.
    """
    payload = {
        'read_permission': False,
        'read_all_permission': False,
        'create_permission': False,
        'update_permission': False,
        'update_all_permission': False,
        'delete_permission': False,
        'delete_all_permission': False,
    }
    response = await async_client.patch(
        f'/v1/authorization/permissions/{role_permission_fixture.id}/',
        json=payload,
        headers={
            'Authorization': f'Bearer {auth_tokens_owner_fixture.access}',
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == str(role_permission_fixture.id)
    assert response_data['role']['id'] == str(
        role_permission_fixture.role_id
    )
    assert response_data['resource']['id'] == str(
        role_permission_fixture.resource_id
    )
