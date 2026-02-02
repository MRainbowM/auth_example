import pytest
from apps.resources.models import Resource
from apps.users.models import User


@pytest.fixture
async def resource_fixture(
        user_owner_resource_fixture: User,
) -> Resource:
    """
    Фикстура для создания ресурса.

    :param user_fixture: Фикстура пользователя - владелец ресурса.
    :return: Созданный ресурс.
    """
    resource, _ = await Resource.objects.aget_or_create(
        name='Заказы',
        defaults={
            'owner': user_owner_resource_fixture,
        },
    )
    return resource
