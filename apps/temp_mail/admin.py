from django.contrib import admin
from apps.temp_mail.models import TempMail, Message


@admin.register(TempMail)
class TempMailAdmin(admin.ModelAdmin):
    list_display = (
        'temp_email',
        'email_username',
        'email_domain',
        'user'
    )
    list_filter = (
        'email_domain',
        'user',
    )
    search_fields = (
        'temp_email',
        'email_username',
        'email_domain',
        'user__username',
    )
    ordering = (
        'temp_email',
        'email_username',
        'email_domain',
        'user',
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'message_id',
        'from_email',
        'subject',
        'body',
        'retrieving_date',
        'user',
    )
    list_filter = (
        'user',
    )
    search_fields = (
        'temp_email',
        'message_id',
        'from_email',
        'subject',
        'body',
        'retrieving_date',
        'user__username',
    )
    ordering = (
        'message_id',
        'from_email',
        'subject',
        'body',
        'retrieving_date',
        'user',
    )
