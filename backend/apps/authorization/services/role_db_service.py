from apps.authorization.models import Role
from apps.users.models import User


class RoleDBService:
    """
    Сервис для работы с ролями.
    """

    def __init__(self):
        self.model = Role

    async def get_roles_by_user(self, user: User) -> list[Role]:
        """
        Получение ролей пользователя.

        :param user: Пользователь.
        :return: Роли пользователя.
        """
        qs = self.model.objects.filter(user_roles__user=user).all()
        return [obj async for obj in qs]


role_db_service = RoleDBService()
