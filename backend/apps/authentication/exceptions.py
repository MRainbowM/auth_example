from typing import Optional


class InvalidCredentialsError(Exception):
    default_message = 'Неверные учетные данные'

    def __init__(self, message: Optional[str] = None):
        self.message = message or self.default_message
        super().__init__(message)
