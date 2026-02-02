from django.contrib import admin

from ..models import UserRole


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    readonly_fields = ('id', 'created_at', 'updated_at')
