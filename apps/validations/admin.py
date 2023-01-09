from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from rest_framework.fields import JSONField

from apps.validations.models import Email, IMEI, JwtToken


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("email", "user", "is_valid", "created_at", "updated_at")
    list_filter = ("is_valid", "created_at", "updated_at")
    search_fields = ("email", "user__username", "user__email")


@admin.register(IMEI)
class IMEIAdmin(admin.ModelAdmin):
    list_display = ("imei", "user", "is_valid", "created_at", "updated_at")
    list_filter = ("is_valid", "created_at", "updated_at")
    search_fields = ("imei", "user__username", "user__email")


@admin.register(JwtToken)
class JWTTokenAdmin(admin.ModelAdmin):
    list_display = ("jwt_token", "header", "user", "created_at", "updated_at")
    fields = ("jwt_token", "header", "user")
    search_fields = ("jwt_token", "user__username", "user__email")
    list_filter = ("created_at", "updated_at")
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
