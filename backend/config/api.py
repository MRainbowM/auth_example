from apps.authentication.api import router as authentication_router

from apps.users.api import router as users_router
from ninja import NinjaAPI

api = NinjaAPI(
    urls_namespace='api',
    docs_url='docs',
    openapi_url='openapi.json',
)

api.add_router('/v1/authentication/', authentication_router)
api.add_router('/v1/users/', users_router)
