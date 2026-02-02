from config.jwt_auth import jwt_auth
from ninja import Router

from .schemas import PermissionOutSchema
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
