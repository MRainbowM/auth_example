import bcrypt


class PasswordService:
    async def hash_password(self, password: str) -> str:
        """
        Хэширование пароля.

        :param password: Пароль пользователя.
        :return: Хэшированный пароль.
        """
        return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt(),
        ).decode()

    async def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Проверка пароля.

        :param password: Пароль пользователя.
        :param hashed_password: Хэшированный пароль.
        :return: True, если пароль верный, False - если неверный.
        """
        return bcrypt.checkpw(password.encode(), hashed_password.encode())


password_service = PasswordService()
