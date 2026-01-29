from django.contrib import admin

from ..models import TokenBlacklist


@admin.register(TokenBlacklist)
class TokenBlacklistAdmin(admin.ModelAdmin):
    list_display = ('token_jti', 'id', 'created_at', 'updated_at')
    readonly_fields = ('token_jti', 'id', 'created_at', 'updated_at')
