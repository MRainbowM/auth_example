from apps.authentication.api import router as authentication_router
from apps.authorization.api import router as authorization_router
from apps.resources.api import router as resources_router
from apps.users.api import router as users_router
from ninja import NinjaAPI

api = NinjaAPI(
    urls_namespace='api',
    docs_url='docs',
    openapi_url='openapi.json',
)

api.add_router('/v1/authentication/', authentication_router)
api.add_router('/v1/authorization/', authorization_router)
api.add_router('/v1/resources/', resources_router)
api.add_router('/v1/users/', users_router)
