from apps.users.exeptions import UserNotFound
from apps.users.models import User
from apps.users.services.password_service import password_service
from apps.users.services.user_db_service import user_db_service

from ..exceptions import InvalidCredentialsError


class AuthenticationService:

    async def authenticate_user(
            self,
            email: str,
            password: str
    ) -> User:
        """
        Аутентификация пользователя.

        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :return: Пользователь.
        :raises InvalidCredentialsError: Если пользователь не найден / неактивен / пароль неверный.
        """
        try:
            user = await user_db_service.get_user_by_email(email)
        except UserNotFound:
            raise InvalidCredentialsError()

        if user.is_active is False:
            # Пользователь удален / неактивен
            raise InvalidCredentialsError()

        is_valid_password = await password_service.verify_password(
            password=password,
            hashed_password=user.password_hash
        )
        if not is_valid_password:
            raise InvalidCredentialsError()

        return user


authentication_service = AuthenticationService()
