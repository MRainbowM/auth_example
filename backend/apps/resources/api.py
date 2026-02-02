from uuid import UUID

from config.jwt_auth import jwt_auth
from ninja import Router

from .schemas import ResourceOutSchema
from .services.api_service import resource_api_service

router = Router(tags=['resources'])


@router.get(
    '/',
    response={200: list[ResourceOutSchema], 401: dict, 403: dict, 404: dict},
    auth=jwt_auth,
    summary='Получение списка всех ресурсов',
    description='Метод доступен только авторизованным пользователям, имеющим право на чтение списка всех ресурсов; '
                ' или пользователями - администраторам. Владельцы ресурса могут получить доступ к своему ресурсу.'
)
async def get_all_resources(request):
    return await resource_api_service.get_all_resources(user=request.auth.user)


@router.get(
    '/{resource_id}/',
    response={200: ResourceOutSchema, 401: dict, 403: dict, 404: dict},
    auth=jwt_auth,
    summary='Получение ресурса по id',
    description='Метод доступен только авторизованным пользователям. '
                'Ресурс может получить владелец ресурса или пользователь с соответствующими правами доступа.',
)
async def get_resource_by_id(request, resource_id: UUID):
    return await resource_api_service.get_resource_by_id(
        resource_id=resource_id,
        user=request.auth.user,
    )
