from django.urls import path

from . import views

app_name = 'telegram_bot'

urlpatterns = [
    path('configurar/', views.TelegramConfigView.as_view(), name='configurar'),
    path(
        'api/validate-token/',
        views.api_validate_token,
        name='api_validate_token',
    ),
    path(
        'api/detect-chat-id/',
        views.api_detect_chat_id,
        name='api_detect_chat_id',
    ),
    path('api/save-config/', views.api_save_config, name='api_save_config'),
    path('api/disconnect/', views.api_disconnect, name='api_disconnect'),
    path('webhook/', views.telegram_webhook, name='webhook'),
    path(
        'htmx/dashboard-parcial/',
        views.dashboard_partial,
        name='htmx_dashboard_parcial',
    ),
]
