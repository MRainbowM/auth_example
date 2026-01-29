from typing import Optional
from uuid import UUID

from ninja import Schema
from pydantic import BaseModel, EmailStr


class RegisterSchema(Schema):
    """
    Схема для регистрации пользователя.
    """
    email: EmailStr
    password: str
    password_repeat: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None


class UserOutSchema(Schema):
    """
    Схема пользователя для вывода.
    """
    id: UUID
    email: str
    first_name: str
    last_name: str
    patronymic: str


class LoginSchema(Schema):
    """
    Схема для входа в систему.
    """
    email: EmailStr
    password: str
