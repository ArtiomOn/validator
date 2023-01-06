from django.contrib import admin
from apps.users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_staff", "is_superuser", "updated_at", "created_at")
    list_filter = ("is_active", "is_staff", "updated_at", "created_at")
    search_fields = ("email", "updated_at", "created_at")
    ordering = ("email", "updated_at", "created_at")
