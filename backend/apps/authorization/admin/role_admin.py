from django.contrib import admin

from ..models import Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
