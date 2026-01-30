from typing import Optional
from uuid import UUID

from apps.users.models import User
from ninja.errors import HttpError

from .user_db_service import user_db_service


class UsersAPIService:
    async def get_user(self, user_id: UUID) -> User:
        """
        Получение информации о пользователе.

        :param user_id: ID пользователя.
        :return: Информация о пользователе.
        :raises HttpError(404): Если пользователь не найден.
        """
        user = await user_db_service.get_user_by_id(user_id)
        if not user:
            raise HttpError(
                status_code=404,
                message='Пользователь не найден.',
            )
        return user

    async def update_user(
            self,
            user_id: UUID,
            first_name: Optional[str] = None,
            last_name: Optional[str] = None,
            patronymic: Optional[str] = None,
    ) -> User:
        """
        Обновление информации о пользователе.

        :param user_id: ID пользователя.
        :param first_name: Имя пользователя.
        :param last_name: Фамилия пользователя.
        :param patronymic: Отчество пользователя.
        :return: Обновленный пользователь.
        """
        user = await user_db_service.get_user_by_id(user_id)
        if not user:
            raise HttpError(
                status_code=404,
                message='Пользователь не найден.',
            )
        return await user_db_service.update_user(
            user=user,
            first_name=first_name,
            last_name=last_name,
            patronymic=patronymic,
        )


users_api_service = UsersAPIService()
