from django.contrib import admin

from ..models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_at', 'updated_at')
    readonly_fields = ('id', 'created_at', 'updated_at')
