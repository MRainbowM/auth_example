from uuid import UUID

from ninja import Schema


class RoleOutSchema(Schema):
    """
    Схема роли.
    """
    id: UUID
    name: str


class ResourceOutSchema(Schema):
    """
    Схема ресурса.
    """
    id: UUID
    name: str


class PermissionOutSchema(Schema):
    """
    Схема прав доступа.
    """
    id: UUID
    role: RoleOutSchema
    resource: ResourceOutSchema
    read_permission: bool
    read_all_permission: bool
    create_permission: bool
    update_permission: bool
    update_all_permission: bool
    delete_permission: bool
    delete_all_permission: bool


class PermissionUpdateSchema(Schema):
    """
    Схема обновления прав доступа.
    """
    read_permission: bool
    read_all_permission: bool
    create_permission: bool
    update_permission: bool
    update_all_permission: bool
    delete_permission: bool
    delete_all_permission: bool
