import pytest
from apps.authentication.services.jwt_service import AuthTokens
from apps.authorization.models import RolePermission, UserRole, Role
from apps.resources.models import Resource
from apps.users.models import User

from .conftest import async_client


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_all_resources(
        resource_fixture: Resource,
        user_fixture: User,
        auth_tokens_fixture: AuthTokens,
):
    """
    Тест получения списка всех ресурсов пользователем, у которого есть право на чтение списка всех ресурсов.
    """
    # Удаление ресурсов, кроме тестируемого
    await Resource.objects.exclude(id=resource_fixture.id).adelete()

    # Установка права на чтение списка всех ресурсов
    user_fixture.is_admin = True
    await user_fixture.asave()

    response = await async_client.get(
        '/v1/resources/',
        headers={
            'Authorization': f'Bearer {auth_tokens_fixture.access}',
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]['id'] == str(resource_fixture.id)
    assert response_data[0]['name'] == resource_fixture.name


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_all_resources_owner(
        resource_fixture: Resource,
        auth_tokens_owner_fixture: AuthTokens,
):
    """
    Тест получения списка всех ресурсов пользователем, который является владельцем ресурса.

    :param resource_fixture: Фикстура ресурса.
    :param auth_tokens_owner_fixture: Фикстура токенов авторизации пользователя, который является владельцем ресурса.
    """
    response = await async_client.get(
        '/v1/resources/',
        headers={
            'Authorization': f'Bearer {auth_tokens_owner_fixture.access}',
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]['id'] == str(resource_fixture.id)
    assert response_data[0]['name'] == resource_fixture.name


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_all_resources_not_allowed(
        resource_fixture: Resource,
        user_fixture: User,
        auth_tokens_fixture: AuthTokens,
):
    """
    Тест получения списка всех ресурсов пользователем, у которого нет права на чтение списка всех ресурсов.
    """
    # Установка статуса пользователя не администратор
    user_fixture.is_admin = False
    await user_fixture.asave()

    # Удаление ролей пользователя
    await UserRole.objects.filter(user=user_fixture).adelete()

    response = await async_client.get(
        '/v1/resources/',
        headers={
            'Authorization': f'Bearer {auth_tokens_fixture.access}',
        },
    )
    assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_resource_by_id(
        resource_fixture: Resource,
        user_fixture: User,
        auth_tokens_fixture: AuthTokens,
        role_permission_fixture: RolePermission,
        role_fixture: Role,
):
    """
    Тест получения ресурса по id пользователем, у которого есть право на чтение ресурса.

    :param resource_fixture: Фикстура ресурса.
    :param user_fixture: Фикстура пользователя.
    :param auth_tokens_fixture: Фикстура токенов авторизации.
    :param role_permission_fixture: Фикстура права доступа.
    :param role_fixture: Фикстура роли.
    """
    # Установка права на чтение ресурса
    role_permission_fixture.read_permission = True
    await role_permission_fixture.asave()

    # Установка роли пользователя
    await UserRole.objects.aget_or_create(
        user=user_fixture,
        role=role_fixture,
    )

    response = await async_client.get(
        f'/v1/resources/{resource_fixture.id}/',
        headers={
            'Authorization': f'Bearer {auth_tokens_fixture.access}',
        },
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == str(resource_fixture.id)
    assert response_data['name'] == resource_fixture.name


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_resource_by_id_owner(
        resource_fixture: Resource,
        auth_tokens_owner_fixture: AuthTokens,
):
    """
    Тест получения ресурса по id пользователем, который является владельцем ресурса.

    :param resource_fixture: Фикстура ресурса.
    :param auth_tokens_owner_fixture: Фикстура токенов авторизации.
    """
    response = await async_client.get(
        f'/v1/resources/{resource_fixture.id}/',
        headers={
            'Authorization': f'Bearer {auth_tokens_owner_fixture.access}',
        },
    )
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_resource_by_id_not_allowed(
        resource_fixture: Resource,
        user_fixture: User,
        auth_tokens_fixture: AuthTokens,
):
    """
    Тест получения ресурса по id пользователем, у которого нет права на чтение ресурса.

    :param resource_fixture: Фикстура ресурса.
    :param user_fixture: Фикстура пользователя.
    :param auth_tokens_fixture: Фикстура токенов авторизации.
    """
    # Удаление ролей пользователя
    await UserRole.objects.filter(user=user_fixture).adelete()

    response = await async_client.get(
        f'/v1/resources/{resource_fixture.id}/',
        headers={
            'Authorization': f'Bearer {auth_tokens_fixture.access}',
        },
    )
    assert response.status_code == 403
