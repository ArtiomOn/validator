from django.contrib import admin

from apps.methods.models import Email, IMEI


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'user',
        'is_valid',
        'created_at',
        'updated_at'
    )
    list_filter = (
        'is_valid',
        'created_at',
        'updated_at'
    )
    search_fields = (
        'email',
        'user__username',
        'user__email'
    )


@admin.register(IMEI)
class IMEIAdmin(admin.ModelAdmin):
    list_display = (
        'imei',
        'user',
        'is_valid',
        'created_at',
        'updated_at'
    )
    list_filter = (
        'is_valid',
        'created_at',
        'updated_at'
    )
    search_fields = (
        'imei',
        'user__username',
        'user__email'
    )
