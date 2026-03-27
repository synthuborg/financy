import datetime
import re
from decimal import Decimal
from io import BytesIO

# pylint: disable=no-member

import requests
from django.conf import settings
from django.db.models import Sum

from finances.models import Category, Transaction


class TelegramService:
    BASE = 'https://api.telegram.org/bot{token}/{method}'
    FILE_BASE = 'https://api.telegram.org/file/bot{token}/{file_path}'

    def __init__(self, token: str):
        self.token = token

    def _request(
        self,
        method: str,
        payload: dict | None = None,
        http_method: str = 'POST',
    ) -> dict:
        url = self.BASE.format(token=self.token, method=method)
        if http_method == 'GET':
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=payload or {}, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_me(self) -> dict:
        return self._request('getMe', http_method='GET')

    def get_updates(self) -> dict:
        return self._request('getUpdates', http_method='GET')

    def set_webhook(self, webhook_url: str) -> dict:
        return self._request('setWebhook', {'url': webhook_url})

    def delete_webhook(self) -> dict:
        return self._request('deleteWebhook')

    def set_commands(self) -> dict:
        commands = {
            'commands': [
                {'command': 'listar', 'description': 'Ver últimas transações'},
                {'command': 'saldo', 'description': 'Ver saldo atual'},
                {
                    'command': 'excluir',
                    'description': 'Excluir último lançamento',
                },
                {'command': 'ajuda', 'description': 'Ver ajuda'},
            ]
        }
        return self._request('setMyCommands', commands)

    def send_message(
        self,
        chat_id: str | int,
        text: str,
        parse_mode: str = 'HTML',
    ) -> dict:
        if len(text) > 4096:
            text = f'{text[:4090]}\n...'
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': parse_mode,
        }
        return self._request('sendMessage', payload)

    def get_file(self, file_id: str) -> dict:
        """Resolve metadata for Telegram file id."""
        url = self.BASE.format(token=self.token, method='getFile')
        response = requests.get(url, params={'file_id': file_id}, timeout=10)
        response.raise_for_status()
        return response.json()

    def download_file(self, file_path: str) -> bytes:
        """Download a Telegram-hosted file and return raw bytes."""
        url = self.FILE_BASE.format(token=self.token, file_path=file_path)
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        return response.content

    def transcribe_audio(
        self,
        audio_bytes: bytes,
        filename: str = 'audio.ogg',
        mime_type: str = 'audio/ogg',
    ) -> dict:
        """Transcribe audio using OpenAI audio transcriptions API."""
        api_key = getattr(settings, 'OPENAI_API_KEY', '')
        if not api_key:
            return {
                'ok': False,
                'error': 'OPENAI_API_KEY não configurada.',
            }

        audio_stream = BytesIO(audio_bytes)
        audio_stream.name = filename
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {
            'model': 'gpt-4o-mini-transcribe',
            'language': 'pt',
            'response_format': 'json',
        }
        files = {'file': (filename, audio_stream, mime_type)}

        response = requests.post(
            'https://api.openai.com/v1/audio/transcriptions',
            headers=headers,
            data=data,
            files=files,
            timeout=45,
        )

        if response.status_code >= 400:
            return {
                'ok': False,
                'error': f'Falha na transcrição (HTTP {response.status_code}).',
            }

        payload = response.json()
        transcribed_text = (payload.get('text') or '').strip()
        if not transcribed_text:
            return {
                'ok': False,
                'error': 'Não foi possível extrair texto do áudio.',
            }

        return {'ok': True, 'text': transcribed_text}

    def transcribe_telegram_audio(
        self,
        file_id: str,
        filename: str = 'audio.ogg',
        mime_type: str = 'audio/ogg',
    ) -> dict:
        """Resolve, download and transcribe a Telegram audio/voice file."""
        file_info = self.get_file(file_id)
        if not file_info.get('ok'):
            return {
                'ok': False,
                'error': 'Não foi possível obter o arquivo de áudio no Telegram.',
            }

        file_path = file_info.get('result', {}).get('file_path')
        if not file_path:
            return {
                'ok': False,
                'error': 'Arquivo sem file_path retornado pelo Telegram.',
            }

        audio_bytes = self.download_file(file_path)
        return self.transcribe_audio(
            audio_bytes=audio_bytes,
            filename=filename,
            mime_type=mime_type,
        )


class NLPService:
    DESPESA_PATTERNS = [
        (
            r'gastei\s+([\d]+[\.,]?\d*)\s+(?:reais?\s+)?'
            r'(?:com\s+|n[oa]\s+|em\s+)?(.+)'
        ),
        r'paguei\s+([\d]+[\.,]?\d*)\s+(?:reais?\s+)?(?:de\s+|n[oa]\s+)?(.+)',
        r'despesa\s+(?:de\s+)?([\d]+[\.,]?\d*)\s+(.+)',
    ]
    RECEITA_PATTERNS = [
        r'recebi\s+([\d]+[\.,]?\d*)\s+(?:reais?\s+)?(?:de\s+)?(.+)',
        r'ganhei\s+([\d]+[\.,]?\d*)\s+(?:reais?\s+)?(?:de\s+)?(.+)',
        r'entrou\s+([\d]+[\.,]?\d*)\s+(?:reais?\s+)?(?:de\s+)?(.+)',
    ]

    def __init__(self, user):
        self.user = user

    def processar(self, texto: str) -> dict:
        texto_normalizado = (texto or '').strip().lower()

        if texto_normalizado in ('/listar', 'listar'):
            return {'acao': 'listar'}
        if texto_normalizado in ('/saldo', 'saldo', 'quanto tenho'):
            return {'acao': 'saldo'}
        if texto_normalizado in (
            '/excluir',
            'excluir ultimo',
            'excluir último',
        ):
            return {'acao': 'excluir'}
        if texto_normalizado in ('/ajuda', '/start', 'ajuda'):
            return {'acao': 'ajuda'}

        for pattern in self.DESPESA_PATTERNS:
            match = re.search(pattern, texto_normalizado)
            if match:
                return {
                    'acao': 'criar',
                    'tipo': 'saida',
                    'valor': float(match.group(1).replace(',', '.')),
                    'descricao': match.group(2).strip(),
                }

        for pattern in self.RECEITA_PATTERNS:
            match = re.search(pattern, texto_normalizado)
            if match:
                return {
                    'acao': 'criar',
                    'tipo': 'entrada',
                    'valor': float(match.group(1).replace(',', '.')),
                    'descricao': match.group(2).strip(),
                }

        return {'acao': 'ajuda'}

    def _categorizar_por_keywords(self, descricao: str):
        categorias = Category.objects.filter(
            usuario=self.user,
        ).exclude(keywords='')
        descricao_lower = descricao.lower()

        for categoria in categorias:
            for keyword in categoria.get_keywords_list():
                if keyword in descricao_lower:
                    return categoria
        return None

    def criar_lancamento(
        self,
        tipo: str,
        valor: float,
        descricao: str,
    ) -> dict:
        categoria = self._categorizar_por_keywords(descricao)
        lancamento = Transaction.objects.create(
            usuario=self.user,
            tipo=tipo,
            valor=Decimal(str(valor)),
            descricao=descricao[:255],
            data=datetime.date.today(),
            categoria=categoria,
        )

        emoji = '📈' if tipo == 'entrada' else '📉'
        return {
            'mensagem': (
                f'✅ Lançamento registrado!\n\n'
                f'{emoji} <b>Descrição:</b> {lancamento.descricao}\n'
                f'💰 <b>Valor:</b> R$ {lancamento.valor:.2f}\n'
                f'📅 <b>Data:</b> {lancamento.data:%d/%m/%Y}\n'
                f'🆔 <b>ID:</b> #{lancamento.id}'
            )
        }

    def listar_lancamentos(self, limite: int = 5) -> dict:
        lancamentos = (
            Transaction.objects.filter(usuario=self.user)
            .select_related('categoria')
            .order_by('-data', '-pk')[:limite]
        )

        total_entradas = (
            Transaction.objects.filter(usuario=self.user, tipo='entrada')
            .aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        )
        total_saidas = (
            Transaction.objects.filter(usuario=self.user, tipo='saida')
            .aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        )
        saldo = total_entradas - total_saidas

        if not lancamentos:
            return {'mensagem': 'Nenhum lançamento encontrado.'}

        linhas = ['📋 <b>Últimos lançamentos:</b>\n']
        for item in lancamentos:
            emoji = '📈' if item.tipo == 'entrada' else '📉'
            linhas.append(
                (
                    f'{emoji} R$ {item.valor:.2f} - '
                    f'{item.descricao[:40]} ({item.data:%d/%m})'
                )
            )
        linhas.append(f'\n💰 <b>Saldo total:</b> R$ {saldo:.2f}')
        return {'mensagem': '\n'.join(linhas)}

    def ver_saldo(self) -> dict:
        total_entradas = (
            Transaction.objects.filter(usuario=self.user, tipo='entrada')
            .aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        )
        total_saidas = (
            Transaction.objects.filter(usuario=self.user, tipo='saida')
            .aggregate(total=Sum('valor'))['total'] or Decimal('0.00')
        )
        saldo = total_entradas - total_saidas

        return {
            'mensagem': (
                '📊 <b>Saldo atual:</b>\n\n'
                f'📈 Entradas: R$ {total_entradas:.2f}\n'
                f'📉 Saídas: R$ {total_saidas:.2f}\n'
                f'💰 <b>Saldo: R$ {saldo:.2f}</b>'
            )
        }

    def excluir_ultimo(self) -> dict:
        ultimo = (
            Transaction.objects.filter(usuario=self.user)
            .order_by('-data', '-pk')
            .first()
        )
        if not ultimo:
            return {'mensagem': '❌ Nenhum lançamento para excluir.'}

        descricao = ultimo.descricao
        valor = ultimo.valor
        ultimo.delete()
        return {
            'mensagem': (
                f'🗑️ Lançamento removido: {descricao} '
                f'(R$ {valor:.2f})'
            )
        }

    @staticmethod
    def mensagem_ajuda() -> str:
        return (
            '🤖 <b>Comandos disponíveis</b>\n\n'
            '• <code>gastei 50 no mercado</code>\n'
            '• <code>recebi 3000 de salário</code>\n'
            '• <code>/listar</code>\n'
            '• <code>/saldo</code>\n'
            '• <code>/excluir</code>\n'
            '• <code>/ajuda</code>'
        )
