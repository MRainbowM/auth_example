from config.jwt_auth import jwt_auth
from ninja import Router

from .schemas import (
    RegisterSchema,
    UserOutSchema,
    LoginSchema,
    AuthTokensOutSchema,
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
    response={200: AuthTokensOutSchema, 401: dict},
    summary='Вход в систему',
)
async def login(request, data: LoginSchema):
    return await authentication_api_service.login(
        password=data.password,
        email=data.email,
    )


@router.post(
    '/logout/',
    response={204: None, 401: dict},
    auth=jwt_auth,
    summary='Выход из системы',
)
async def logout(request):
    await authentication_api_service.logout(
        token_data=request.auth.token_data
    )
    return 204, None
