from config.jwt_auth import jwt_auth
from ninja import Router

from .schemas import UserOutSchema, UserUpdateSchema
from .services.users_api_service import users_api_service

router = Router(tags=['users'])


@router.get(
    '/me/',
    response={200: UserOutSchema, 401: dict, 404: dict},
    summary='Получение информации о текущем пользователе',
    auth=jwt_auth,
)
async def get_me(request):
    return await users_api_service.get_user(
        user_id=request.auth.id,
    )


@router.patch(
    '/me/',
    response={200: UserOutSchema, 401: dict, 404: dict},
    summary='Обновление информации о текущем пользователе',
    auth=jwt_auth,
)
async def update_me(request, data: UserUpdateSchema):
    return await users_api_service.update_user(
        user_id=request.auth.id,
        first_name=data.first_name,
        last_name=data.last_name,
        patronymic=data.patronymic,
    )
