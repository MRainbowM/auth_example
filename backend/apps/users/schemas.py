from typing import Optional
from uuid import UUID

from ninja import Schema


class UserOutSchema(Schema):
    id: UUID
    email: str
    first_name: str
    last_name: str
    patronymic: str


class UserUpdateSchema(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
