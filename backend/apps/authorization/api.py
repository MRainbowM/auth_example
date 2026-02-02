from uuid import UUID

from config.jwt_auth import jwt_auth
from ninja import Router

from .schemas import PermissionOutSchema
from .schemas import PermissionUpdateSchema
from .services.api_service import authorization_api_service

router = Router(tags=['authorization'])


@router.get(
    '/permissions/',
    response={200: list[PermissionOutSchema], 401: dict, 403: dict},
    summary='Получение списка прав доступа',
    auth=jwt_auth,
    description='Метод доступен только админам системы.',
)
async def get_permissions(request):
    return await authorization_api_service.get_permissions(
        user=request.auth.user
    )


@router.patch(
    '/permissions/{permission_id}/',
    response={200: PermissionOutSchema, 401: dict, 403: dict, 404: dict},
    summary='Обновление права доступа',
    auth=jwt_auth,
    description='Метод доступен только админам системы. '
                'Владелец ресурса может обновлять права доступа к своим ресурсам.',
)
async def update_permission(request, permission_id: UUID, data: PermissionUpdateSchema):
    return await authorization_api_service.update_permission(
        user=request.auth.user,
        data=data,
        permission_id=permission_id,
    )
