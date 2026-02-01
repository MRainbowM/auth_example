from typing import Optional

from apps.users.exeptions import UserAlreadyExists
from apps.users.models import User
from apps.users.services.user_db_service import user_db_service
from ninja.errors import HttpError

from .authentication_service import authentication_service
from .jwt_service import jwt_service, AuthTokens
from .token_blacklist_db_service import token_blacklist_db_service
from ..dataclasses import AuthTokenPayload
from ..exceptions import InvalidCredentialsError


class AuthenticationAPIService:
    async def register(
            self,
            email: str,
            password: str,
            password_repeat: str,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            patronymic: Optional[str] = None,
    ) -> User:
        """
        Регистрация пользователя.

        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :param password_repeat: Повтор пароля пользователя.
        :param first_name: Имя пользователя.
        :param last_name: Фамилия пользователя.
        :param patronymic: Отчество пользователя.
        :return: Созданный пользователь.
        :raises HttpError(400): Если пароли не совпадают.
        """

        if password != password_repeat:
            raise HttpError(
                status_code=400,
                message='Пароли не совпадают',
            )

        try:
            user = await user_db_service.create(
                email=email,
                password=password,
                first_name=first_name or '',
                last_name=last_name or '',
                patronymic=patronymic or '',
            )
            return user
        except UserAlreadyExists as e:
            raise HttpError(status_code=400, message=e.message)

    async def login(self, password: str, email: str) -> AuthTokens:
        """
        Вход в систему по email и паролю.

        :param password: Пароль пользователя.
        :param email: Email пользователя.
        :return: Токен аутентификации.
        """
        try:
            user = await authentication_service.authenticate_user(
                password=password,
                email=email,
            )
        except InvalidCredentialsError as e:
            raise HttpError(
                status_code=401,
                message=e.message,
            )
        auth_tokens = await jwt_service.create_auth_tokens(user)
        return auth_tokens

    async def logout(self, token_data: AuthTokenPayload) -> None:
        """
        Выход из системы.

        :param token_data: данные токена.
        :return: None.
        """
        await token_blacklist_db_service.add_token_to_blacklist(token_jti=token_data.jti)


authentication_api_service = AuthenticationAPIService()
