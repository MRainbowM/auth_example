from uuid import UUID

from ninja import Schema


class ResourceOutSchema(Schema):
    """
    Схема ресурса для вывода.
    """
    id: UUID
    name: str
