from apps.authorization.models import UserRole
from django.contrib import admin

from ..models import User


class RoleInline(admin.TabularInline):
    model = UserRole
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'first_name', 'last_name',
        'patronymic', 'is_active', 'is_admin', 'id'
    )
    readonly_fields = ('id', 'created_at', 'updated_at')

    inlines = [RoleInline]
