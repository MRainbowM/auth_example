"""
Настройки JWT токенов.
"""
from .django_settings import env

# Время действия access токена в секундах
JWT_ACCESS_TOKEN_LIFETIME = 30 * 60  # 30 минут
# Время действия refresh токена в секундах
JWT_REFRESH_TOKEN_LIFETIME = 60 * 60 * 24 * 7  # 7 дней

JWT_PUBLIC_KEY = env.str('JWT_PUBLIC_KEY')

JWT_PRIVATE_KEY = env.str('JWT_PRIVATE_KEY')

JWT_ALGORITHM = env.str('JWT_ALGORITHM', 'PS256')
