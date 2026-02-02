import pytest
from apps.authentication.services.jwt_service import AuthTokens
from apps.authorization.models.resource_model import Resource
from apps.authorization.models.role_model import Role
from apps.authorization.models.role_permission_model import RolePermission
from apps.users.models import User

from .conftest import async_client


@pytest.mark.django_db
@pytest.mark.asyncio
async def test_get_permissions(
        user_fixture: User,
        auth_tokens_fixture: AuthTokens,
):
    """
    Тест получения списка прав доступа.

    :param user_fixture: Фикстура пользователя.
    :param auth_tokens_fixture: Фикстура токенов авторизации.
    """
    # Установка роли администратора
    user_fixture.is_admin = True
    await user_fixture.asave()

    # Создание роли менеджера
    role = await Role.objects.acreate(
        name='Менеджер'
    )

    # Создание ресурса
    resource = await Resource.objects.acreate(
        name='Заказы',
        owner=user_fixture,
    )

    # Создание правила доступа
    role_permission = await RolePermission.objects.acreate(
        role=role,
        resource=resource,
        read_permission=True,
        read_all_permission=True,
        create_permission=True,
        update_permission=True,
        update_all_permission=False,
        delete_permission=False,
        delete_all_permission=False,
    )

    response = await async_client.get(
        '/v1/authorization/permissions/',
        headers={
            'Authorization': f'Bearer {auth_tokens_fixture.access}',
        },
    )

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 1
    assert response_data[0]['id'] == str(role_permission.id)
    assert response_data[0]['role']['name'] == role.name
    assert response_data[0]['resource']['name'] == resource.name
    assert response_data[0]['read_permission'] == True
    assert response_data[0]['read_all_permission'] == True
    assert response_data[0]['create_permission'] == True
    assert response_data[0]['update_permission'] == True
    assert response_data[0]['update_all_permission'] == False
    assert response_data[0]['delete_permission'] == False
    assert response_data[0]['delete_all_permission'] == False


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
