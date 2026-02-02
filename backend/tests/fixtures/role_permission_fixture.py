import pytest

from apps.authorization.models import Role, RolePermission
from apps.resources.models import Resource


@pytest.fixture
async def role_permission_fixture(
        role_fixture: Role,
        resource_fixture: Resource,
) -> RolePermission:
    """
    Фикстура для создания права доступа.
    """
    role_permission, _ = await RolePermission.objects.aget_or_create(
        role=role_fixture,
        resource=resource_fixture,
        defaults={
            'read_permission': True,
            'read_all_permission': True,
            'create_permission': True,
            'update_permission': True,
            'update_all_permission': False,
            'delete_permission': False,
            'delete_all_permission': False,
        },
    )
    return role_permission
