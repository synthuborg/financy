import importlib

from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver

from finances.models import Transaction
from finances.services import evaluate_and_dispatch_budget_alerts


def _resolve_channel_layer():
    try:
        channels_layers = importlib.import_module('channels.layers')
    except ModuleNotFoundError:
        return None
    return channels_layers.get_channel_layer()


@receiver(post_save, sender=Transaction)
def push_dashboard_update_on_transaction(sender, instance, created, **kwargs):
    if not created:
        return

    channel_layer = _resolve_channel_layer()
    if channel_layer is None:
        return

    group_name = f'dashboard_user_{instance.usuario_id}'
    async_to_sync(channel_layer.group_send)(
        group_name,
        {'type': 'dashboard.update'},
    )

    evaluate_and_dispatch_budget_alerts(instance)
