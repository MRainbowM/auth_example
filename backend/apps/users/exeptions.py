from typing import Optional


class UserAlreadyExists(Exception):
    default_message = 'Пользователь с таким email уже существует'

    def __init__(
            self,
            message: Optional[str] = None,
    ):
        self.message = message or self.default_message
        super().__init__(message)


class UserNotFound(Exception):
    default_message = 'Пользователь не найден'

    def __init__(
            self,
            message: Optional[str] = None,
    ):
        self.message = message or self.default_message
        super().__init__(message)
