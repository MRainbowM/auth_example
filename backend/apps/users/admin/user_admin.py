from django.contrib import admin

from ..models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email', 'first_name', 'last_name',
        'patronymic', 'is_active', 'id'
    )
    readonly_fields = ('id', 'created_at', 'updated_at')
