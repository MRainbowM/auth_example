from django.contrib import admin

from ..models import RolePermission


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = (
        'role', 'resource', 'read_permission', 'read_all_permission', 'create_permission',
        'update_permission', 'update_all_permission', 'delete_permission', 'delete_all_permission'
    )
    readonly_fields = ('id', 'created_at', 'updated_at')
