from django.contrib import admin
from apps.temp_mail.models import TempMail, Message


@admin.register(TempMail)
class TempMailAdmin(admin.ModelAdmin):
    list_display = (
        "temp_email",
        "email_username",
        "email_domain",
        "user",
        "created_at",
    )
    fields = (
        "temp_email",
        "email_username",
        "email_domain",
        "messages",
        "user"
    )
    list_filter = (
        "email_domain",
        "user",
    )
    search_fields = (
        "temp_email",
        "email_username",
        "email_domain",
    )
    ordering = (
        "temp_email",
        "email_username",
        "email_domain",
        "user",
        "created_at",
    )
    readonly_fields = (
        "created_at",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "message_id",
        "from_email",
        "subject",
        "body",
        "retrieving_date",
        "user",
        "created_at",
    )
    list_filter = (
        "user",
    )
    search_fields = (
        "temp_email",
        "message_id",
        "from_email",
        "subject",
        "retrieving_date",
    )
    ordering = (
        "message_id",
        "from_email",
        "subject",
        "body",
        "retrieving_date",
        "user",
        "created_at",
    )
    readonly_fields = (
        "created_at",
    )
