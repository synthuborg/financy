from django.contrib import admin

from .models import TelegramCredential


@admin.register(TelegramCredential)
class TelegramCredentialAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'bot_username',
        'ativo',
        'created_at',
        'updated_at',
    )
    list_filter = ('ativo',)
    search_fields = ('user__username', 'bot_username', 'chat_id_hash')
    readonly_fields = (
        'token_hash',
        'chat_id_hash',
        'created_at',
        'updated_at',
    )
