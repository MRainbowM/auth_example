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


class RoleCreateSchema(Schema):
    """
    Схема создания роли.
    """
    name: str


class UserRoleCreateSchema(Schema):
    """
    Схема создания связи пользователь↔роль.
    """
    user_id: UUID
    role_id: UUID


class UserOutSchema(Schema):
    """
    Схема пользователя.
    """
    id: UUID
    first_name: str
    last_name: str
    patronymic: str


class UserRoleOutSchema(Schema):
    """
    Схема связи пользователь↔роль.
    """
    id: UUID
    user: UserOutSchema
    role: RoleOutSchema
