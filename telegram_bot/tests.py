import json
from datetime import date
from decimal import Decimal

# pylint: disable=no-member,unused-argument

from django.test import Client
from django.urls import reverse

from finances.models import Transaction
from telegram_bot.models import TelegramCredential
from telegram_bot.services import NLPService


class TestTelegramCredentialModel:
    def test_hash_and_encryption_no_plain_text(self, db, usuario):
        config = TelegramCredential(user=usuario, bot_username='bot_teste')
        config.set_token('123:ABC')
        config.set_chat_id('999888777')
        config.ativo = True
        config.save()

        config.refresh_from_db()
        assert config.token_hash != '123:ABC'
        assert config.chat_id_hash != '999888777'
        assert '123:ABC' not in config.token_encrypted
        assert config.get_token() == '123:ABC'


class TestNLPService:
    def test_parse_and_create_saida(self, db, usuario):
        service = NLPService(usuario)
        parsed = service.processar('gastei 50 no mercado')

        assert parsed['acao'] == 'criar'
        assert parsed['tipo'] == 'saida'

        result = service.criar_lancamento(
            tipo=parsed['tipo'],
            valor=parsed['valor'],
            descricao=parsed['descricao'],
        )

        created = Transaction.objects.get(usuario=usuario)
        assert created.tipo == 'saida'
        assert created.valor == Decimal('50')
        assert 'Lançamento registrado' in result['mensagem']


class TestTelegramEndpoints:
    def test_validate_token_success(self, client_autenticado, monkeypatch):
        def fake_get_me(_self):
            return {
                'ok': True,
                'result': {'username': 'meubot', 'first_name': 'Meu Bot'},
            }

        monkeypatch.setattr(
            'telegram_bot.views.TelegramService.get_me',
            fake_get_me,
        )

        response = client_autenticado.post(
            reverse('telegram_bot:api_validate_token'),
            data=json.dumps({'bot_token': '123:ABC'}),
            content_type='application/json',
        )

        assert response.status_code == 200
        payload = response.json()
        assert payload['sucesso'] is True
        assert payload['username'] == 'meubot'

    def test_save_config_persists_hashes(
        self,
        client_autenticado,
        usuario,
        monkeypatch,
    ):
        monkeypatch.setattr(
            'telegram_bot.views.TelegramService.get_me',
            lambda self: {'ok': True, 'result': {'username': 'meubot'}},
        )
        monkeypatch.setattr(
            'telegram_bot.views.TelegramService.set_commands',
            lambda self: {'ok': True},
        )
        monkeypatch.setattr(
            'telegram_bot.views.TelegramService.set_webhook',
            lambda self, webhook_url: {'ok': True},
        )
        monkeypatch.setattr(
            'telegram_bot.views.TelegramService.send_message',
            lambda self, chat_id, text: {'ok': True},
        )

        response = client_autenticado.post(
            reverse('telegram_bot:api_save_config'),
            data=json.dumps(
                {
                    'bot_token': '123:ABC',
                    'chat_id': '555444333',
                    'bot_username': 'meubot',
                    'webhook_url': 'https://example.com/telegram/webhook/',
                }
            ),
            content_type='application/json',
        )

        assert response.status_code == 200
        assert response.json()['sucesso'] is True

        config = TelegramCredential.objects.get(user=usuario)
        assert config.token_hash
        assert config.chat_id_hash
        assert config.token_encrypted
        assert config.get_token() == '123:ABC'

    def test_webhook_creates_transaction_for_mapped_chat(
        self,
        db,
        client,
        usuario,
        monkeypatch,
    ):
        config = TelegramCredential(user=usuario, bot_username='bot')
        config.set_token('123:ABC')
        config.set_chat_id('112233')
        config.ativo = True
        config.save()

        sent_messages = []

        def fake_send_message(self, chat_id, text, parse_mode='HTML'):
            sent_messages.append((chat_id, text))
            return {'ok': True}

        monkeypatch.setattr(
            'telegram_bot.views.TelegramService.send_message',
            fake_send_message,
        )

        response = client.post(
            reverse('telegram_bot:webhook'),
            data=json.dumps(
                {
                    'message': {
                        'chat': {'id': 112233},
                        'text': 'gastei 10 no cafe',
                    }
                }
            ),
            content_type='application/json',
        )

        assert response.status_code == 200
        assert response.json()['ok'] is True
        assert Transaction.objects.filter(usuario=usuario).count() == 1
        created = Transaction.objects.get(usuario=usuario)
        assert created.tipo == 'saida'
        assert sent_messages

    def test_webhook_ignores_unknown_chat(self, db, client, usuario):
        config = TelegramCredential(user=usuario, bot_username='bot')
        config.set_token('123:ABC')
        config.set_chat_id('998877')
        config.ativo = True
        config.save()

        response = client.post(
            reverse('telegram_bot:webhook'),
            data=json.dumps(
                {
                    'message': {
                        'chat': {'id': 445566},
                        'text': 'recebi 100 de bonus',
                    }
                }
            ),
            content_type='application/json',
        )

        assert response.status_code == 200
        assert response.json()['ok'] is True
        assert Transaction.objects.filter(usuario=usuario).count() == 0

    def test_webhook_voice_transcribed_creates_transaction(
        self,
        db,
        client,
        usuario,
        monkeypatch,
    ):
        config = TelegramCredential(user=usuario, bot_username='bot')
        config.set_token('123:ABC')
        config.set_chat_id('101010')
        config.ativo = True
        config.save()

        sent_messages = []

        monkeypatch.setattr(
            'telegram_bot.views.TelegramService.transcribe_telegram_audio',
            lambda self, file_id, filename='audio.ogg', mime_type='audio/ogg': {
                'ok': True,
                'text': 'gastei 10 no cafe',
            },
        )

        def fake_send_message(self, chat_id, text, parse_mode='HTML'):
            sent_messages.append((chat_id, text))
            return {'ok': True}

        monkeypatch.setattr(
            'telegram_bot.views.TelegramService.send_message',
            fake_send_message,
        )

        response = client.post(
            reverse('telegram_bot:webhook'),
            data=json.dumps(
                {
                    'message': {
                        'chat': {'id': 101010},
                        'voice': {
                            'file_id': 'voice_file_1',
                            'mime_type': 'audio/ogg',
                        },
                    }
                }
            ),
            content_type='application/json',
        )

        assert response.status_code == 200
        assert response.json()['ok'] is True
        assert Transaction.objects.filter(usuario=usuario).count() == 1
        assert sent_messages
        assert 'Entendi:' in sent_messages[0][1]

    def test_webhook_voice_transcription_error_returns_fallback(
        self,
        db,
        client,
        usuario,
        monkeypatch,
    ):
        config = TelegramCredential(user=usuario, bot_username='bot')
        config.set_token('123:ABC')
        config.set_chat_id('202020')
        config.ativo = True
        config.save()

        monkeypatch.setattr(
            'telegram_bot.views.TelegramService.transcribe_telegram_audio',
            lambda self, file_id, filename='audio.ogg', mime_type='audio/ogg': {
                'ok': False,
                'error': 'timeout',
            },
        )

        sent_messages = []

        def fake_send_message(self, chat_id, text, parse_mode='HTML'):
            sent_messages.append((chat_id, text))
            return {'ok': True}

        monkeypatch.setattr(
            'telegram_bot.views.TelegramService.send_message',
            fake_send_message,
        )

        response = client.post(
            reverse('telegram_bot:webhook'),
            data=json.dumps(
                {
                    'message': {
                        'chat': {'id': 202020},
                        'voice': {'file_id': 'voice_file_2'},
                    }
                }
            ),
            content_type='application/json',
        )

        assert response.status_code == 200
        assert response.json()['ok'] is True
        assert Transaction.objects.filter(usuario=usuario).count() == 0
        assert sent_messages
        assert 'Não consegui transcrever seu áudio' in sent_messages[0][1]

    def test_dashboard_partial_requires_auth_and_renders(
        self,
        client_autenticado,
        db,
        usuario,
    ):
        unauth_client = Client()
        unauth = unauth_client.get(
            reverse('telegram_bot:htmx_dashboard_parcial')
        )
        assert unauth.status_code == 302

        Transaction.objects.create(
            usuario=usuario,
            tipo='entrada',
            valor=Decimal('150.00'),
            descricao='Salário',
            data=date.today(),
        )
        auth_response = client_autenticado.get(
            reverse('telegram_bot:htmx_dashboard_parcial')
        )
        assert auth_response.status_code == 200
        assert 'Salário' in auth_response.content.decode('utf-8')

    def test_disconnect_removes_user_config(
        self,
        client_autenticado,
        usuario,
        monkeypatch,
    ):
        config = TelegramCredential(user=usuario, bot_username='bot')
        config.set_token('123:ABC')
        config.set_chat_id('123123')
        config.ativo = True
        config.save()

        monkeypatch.setattr(
            'telegram_bot.views.TelegramService.delete_webhook',
            lambda self: {'ok': True},
        )

        response = client_autenticado.post(
            reverse('telegram_bot:api_disconnect'),
            data=json.dumps({}),
            content_type='application/json',
        )

        assert response.status_code == 200
        assert response.json()['sucesso'] is True
        assert not TelegramCredential.objects.filter(user=usuario).exists()


class TestTelegramServiceAudio:
    def test_transcribe_audio_without_api_key(self, settings):
        settings.OPENAI_API_KEY = ''
        from telegram_bot.services import TelegramService

        result = TelegramService('123:ABC').transcribe_audio(b'audio-bytes')
        assert result['ok'] is False
        assert 'OPENAI_API_KEY' in result['error']
