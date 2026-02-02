from config.jwt_auth import jwt_auth
from ninja import Router

from .schemas import UserOutSchema, UserUpdateSchema
from .services.users_api_service import users_api_service

router = Router(tags=['users'])


@router.get(
    '/',
    response={200: list[UserOutSchema], 401: dict, 403: dict},
    summary='Получение списка пользователей',
    auth=jwt_auth,
    description='Метод доступен только админам системы.',
)
async def get_users(request):
    return await users_api_service.get_users(user=request.auth.user)


@router.get(
    '/me/',
    response={200: UserOutSchema, 401: dict, 404: dict},
    summary='Получение информации о текущем пользователе',
    auth=jwt_auth,
)
async def get_me(request):
    return await users_api_service.get_user(
        user_id=request.auth.user.id,
    )


@router.patch(
    '/me/',
    response={200: UserOutSchema, 401: dict, 404: dict},
    summary='Обновление информации о текущем пользователе',
    auth=jwt_auth,
)
async def update_me(request, data: UserUpdateSchema):
    return await users_api_service.update_user(
        user_id=request.auth.user.id,
        first_name=data.first_name,
        last_name=data.last_name,
        patronymic=data.patronymic,
    )


@router.delete(
    '/me/',
    response={204: None, 401: dict, 404: dict},
    summary='Удаление текущего пользователя',
    auth=jwt_auth,
)
async def delete_me(request):
    await users_api_service.delete_user(
        user=request.auth.user,
        token_data=request.auth.token_data,
    )
    return 204, None
