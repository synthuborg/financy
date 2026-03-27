from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from dashboard import selectors as dashboard_selectors
from finances.services import calculate_balance


class DashboardConsumer(AsyncWebsocketConsumer):
    group_name = ''

    async def connect(self):
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            await self.close()
            return

        self.group_name = f'dashboard_user_{user.id}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name,
            )

    async def dashboard_update(self, event):
        payload = await self._build_dashboard_payload()
        await self.send(text_data=payload)

    @database_sync_to_async
    def _build_dashboard_payload(self):
        user = self.scope['user']
        context = {
            'resumo_mes': dashboard_selectors.obter_resumo_mes_atual(user),
            'ultimas_transacoes': dashboard_selectors.obter_ultimas_transacoes(
                user, limit=20
            ),
            'saldo': calculate_balance(user),
            'dados_evolucao': dashboard_selectors.obter_dados_evolucao_6_meses(
                user
            ),
            'dados_saidas': dashboard_selectors.obter_distribuicao_saidas_mes(
                user
            ),
            'dados_metas': dashboard_selectors.obter_dados_metas(user),
        }
        return render_to_string(
            'dashboard/fragmentos/dashboard_push_update.html',
            context,
        )
