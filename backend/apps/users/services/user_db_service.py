from typing import Optional

from apps.users.models import User
from django.db import IntegrityError

from .password_service import password_service
from ..exeptions import UserAlreadyExists, UserNotFound


class UserDBService:
    def __init__(self):
        self.model = User

    async def create(
            self,
            email: str,
            password: str,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            patronymic: Optional[str] = None,
    ) -> User:
        """
        Создание пользователя.

        :param email: Email пользователя.
        :param password: Пароль пользователя.
        :param first_name: Имя пользователя.
        :param last_name: Фамилия пользователя.
        :param patronymic: Отчество пользователя.

        :return: Созданный пользователь.
        """

        hashed_password = await password_service.hash_password(
            password=password
        )
        try:

            user = await self.model.objects.acreate(
                email=email,
                password_hash=hashed_password,
                first_name=first_name,
                last_name=last_name,
                patronymic=patronymic,
            )

            return user

        except IntegrityError:
            raise UserAlreadyExists

    async def get_user_by_email(self, email: str) -> User:
        """
        Получение пользователя по email.

        :param email: Email пользователя.
        :return: Пользователь.
        :raises UserNotFound: Если пользователь не найден.
        """
        user = await self.model.objects.filter(email=email).afirst()

        if not user:
            raise UserNotFound

        return user


user_db_service = UserDBService()
