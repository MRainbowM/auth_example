"""
Константы для работы с JWT токенами.
"""
from typing import Literal

# Типы токенов
ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'

TOKEN_TYPE_LITERAL = Literal[ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE]
