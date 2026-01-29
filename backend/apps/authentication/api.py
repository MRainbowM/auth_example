from ninja import Router

from .schemas import (
    RegisterSchema,
    UserOutSchema,
    LoginSchema,
)
from .services.api_service import authentication_api_service

router = Router(tags=['authentication'])


@router.post(
    '/register/',
    response={200: UserOutSchema, 400: dict},
    summary='Регистрация пользователя',
)
async def register(request, data: RegisterSchema):
    return await authentication_api_service.register(
        email=data.email,
        password=data.password,
        password_repeat=data.password_repeat,
        first_name=data.first_name,
        last_name=data.last_name,
        patronymic=data.patronymic,
    )


@router.post(
    '/login/',
    summary='Вход в систему',
)
async def login(request, data: LoginSchema):
    return await authentication_api_service.login(
        password=data.password,
        email=data.email,
    )
