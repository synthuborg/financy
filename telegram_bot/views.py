import json
import logging

# pylint: disable=no-member,broad-exception-caught

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from dashboard import selectors as dashboard_selectors
from finances.services import calculate_balance

from .models import TelegramCredential
from .services import NLPService, TelegramService

logger = logging.getLogger(__name__)


class TelegramConfigView(LoginRequiredMixin, TemplateView):
    template_name = 'telegram_bot/configurar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['telegram_config'] = TelegramCredential.objects.filter(
            user=self.request.user
        ).first()
        return context


@login_required
@require_POST
def api_validate_token(request):
    try:
        data = json.loads(request.body or '{}')
        token = (data.get('bot_token') or '').strip()
        if not token:
            return JsonResponse(
                {'sucesso': False, 'mensagem': 'Token obrigatório.'}
            )

        info = TelegramService(token).get_me()
        if not info.get('ok'):
            return JsonResponse(
                {'sucesso': False, 'mensagem': 'Token inválido.'}
            )

        result = info.get('result', {})
        return JsonResponse(
            {
                'sucesso': True,
                'username': result.get('username', ''),
                'bot_name': result.get('first_name', ''),
            }
        )
    except Exception as exc:  # noqa: BLE001
        logger.error('Erro ao validar token do Telegram: %s', exc)
        return JsonResponse(
            {'sucesso': False, 'mensagem': 'Erro ao validar token.'}
        )


@login_required
@require_POST
def api_detect_chat_id(request):
    try:
        data = json.loads(request.body or '{}')
        token = (data.get('bot_token') or '').strip()
        if not token:
            return JsonResponse(
                {'sucesso': False, 'mensagem': 'Token obrigatório.'}
            )

        updates = TelegramService(token).get_updates()
        for item in reversed(updates.get('result', [])):
            message = item.get('message') or item.get('edited_message') or {}
            chat = message.get('chat', {})
            chat_id = chat.get('id')
            if chat_id is not None:
                return JsonResponse({'sucesso': True, 'chat_id': str(chat_id)})

        return JsonResponse(
            {
                'sucesso': False,
                'mensagem': (
                    'Nenhuma mensagem encontrada. Envie uma mensagem '
                    'para o bot e tente novamente.'
                ),
            }
        )
    except Exception as exc:  # noqa: BLE001
        logger.error('Erro ao detectar chat_id no Telegram: %s', exc)
        return JsonResponse(
            {'sucesso': False, 'mensagem': 'Erro ao detectar chat_id.'}
        )


@login_required
@require_POST
def api_save_config(request):
    try:
        data = json.loads(request.body or '{}')
        token = (data.get('bot_token') or '').strip()
        chat_id = (data.get('chat_id') or '').strip()
        bot_username = (data.get('bot_username') or '').strip()
        webhook_url = (data.get('webhook_url') or '').strip()

        if not token or not chat_id:
            return JsonResponse(
                {
                    'sucesso': False,
                    'mensagem': 'Token e chat_id são obrigatórios.',
                }
            )

        if not webhook_url:
            return JsonResponse(
                {
                    'sucesso': False,
                    'mensagem': 'Informe a URL pública do webhook.',
                }
            )

        if not webhook_url.startswith('https://'):
            return JsonResponse(
                {
                    'sucesso': False,
                    'mensagem': 'Webhook deve começar com https://',
                }
            )

        service = TelegramService(token)
        me = service.get_me()
        if not me.get('ok'):
            return JsonResponse(
                {'sucesso': False, 'mensagem': 'Token inválido.'}
            )

        config = TelegramCredential.objects.filter(user=request.user).first()
        if config is None:
            config = TelegramCredential(user=request.user)

        config.set_token(token)
        config.set_chat_id(chat_id)
        config.bot_username = (
            bot_username or me.get('result', {}).get('username', '')
        )
        config.ativo = True
        config.save()

        service.set_commands()
        webhook_result = service.set_webhook(webhook_url)
        if not webhook_result.get('ok'):
            return JsonResponse(
                {
                    'sucesso': False,
                    'mensagem': 'Falha ao registrar webhook no Telegram.',
                }
            )

        service.send_message(
            chat_id=chat_id,
            text=(
                '🎉 <b>Bot conectado com sucesso!</b>\n\n'
                'Envie mensagens como:\n'
                '• <code>gastei 50 no mercado</code>\n'
                '• <code>recebi 3000 de salário</code>\n\n'
                'Comandos: /listar /saldo /excluir /ajuda'
            ),
        )

        return JsonResponse({'sucesso': True})
    except Exception as exc:  # noqa: BLE001
        logger.error('Erro ao salvar configuração do Telegram: %s', exc)
        return JsonResponse(
            {'sucesso': False, 'mensagem': 'Erro ao salvar configuração.'}
        )


@login_required
@require_POST
def api_disconnect(request):
    config = TelegramCredential.objects.filter(user=request.user).first()
    if not config:
        return JsonResponse(
            {'sucesso': False, 'mensagem': 'Configuração não encontrada.'}
        )

    try:
        token = config.get_token()
        TelegramService(token).delete_webhook()
    except Exception as exc:  # noqa: BLE001
        logger.warning('Falha ao remover webhook no disconnect: %s', exc)

    config.delete()
    return JsonResponse({'sucesso': True})


@csrf_exempt
@require_POST
def telegram_webhook(request):
    try:
        payload = json.loads(request.body or '{}')
        message = payload.get('message') or payload.get('edited_message') or {}
        text = (message.get('text') or '').strip()
        voice = message.get('voice') or {}
        audio = message.get('audio') or {}
        chat = message.get('chat', {})
        chat_id = chat.get('id')

        if not chat_id:
            return JsonResponse({'ok': True})

        chat_hash = TelegramCredential.hash_chat_id(str(chat_id))
        config = TelegramCredential.objects.filter(
            chat_id_hash=chat_hash,
            ativo=True,
        ).first()
        if config is None:
            return JsonResponse({'ok': True})

        service = TelegramService(config.get_token())
        nlp = NLPService(config.user)

        audio_file_id = None
        audio_filename = 'audio.ogg'
        audio_mime = 'audio/ogg'

        if voice:
            audio_file_id = voice.get('file_id')
            audio_mime = voice.get('mime_type', 'audio/ogg')
        elif audio:
            audio_file_id = audio.get('file_id')
            audio_filename = audio.get('file_name', 'audio.mp3')
            audio_mime = audio.get('mime_type', 'audio/mpeg')

        transcribed_text = None
        if not text and audio_file_id:
            transcribed = service.transcribe_telegram_audio(
                file_id=audio_file_id,
                filename=audio_filename,
                mime_type=audio_mime,
            )
            if transcribed.get('ok'):
                transcribed_text = transcribed.get('text', '').strip()
                text = transcribed_text
            else:
                logger.warning(
                    'Falha na transcrição de áudio no webhook: %s',
                    transcribed.get('error'),
                )
                response_text = (
                    '🎙️ Não consegui transcrever seu áudio agora.\n\n'
                    'Tente novamente ou envie em texto:\n'
                    '• <code>gastei 50 no mercado</code>\n'
                    '• <code>recebi 3000 de salário</code>'
                )

        if not text and not audio_file_id:
            response_text = NLPService.mensagem_ajuda()
        elif text:
            action = nlp.processar(text)
            if action['acao'] == 'criar':
                response_text = nlp.criar_lancamento(
                    action['tipo'], action['valor'], action['descricao']
                )['mensagem']
            elif action['acao'] == 'listar':
                response_text = nlp.listar_lancamentos()['mensagem']
            elif action['acao'] == 'saldo':
                response_text = nlp.ver_saldo()['mensagem']
            elif action['acao'] == 'excluir':
                response_text = nlp.excluir_ultimo()['mensagem']
            else:
                response_text = NLPService.mensagem_ajuda()

            if transcribed_text:
                response_text = (
                    f'🎙️ <b>Entendi:</b> <code>{transcribed_text[:160]}</code>\n\n'
                    f'{response_text}'
                )
        else:
            response_text = (
                '🎙️ Não consegui transcrever seu áudio agora.\n\n'
                'Envie o lançamento em texto ou tente outro áudio.'
            )

        service.send_message(chat_id=chat_id, text=response_text)
        return JsonResponse({'ok': True})
    except Exception as exc:  # noqa: BLE001
        logger.error(
            'Erro interno no webhook Telegram: %s',
            exc,
            exc_info=True,
        )
        return JsonResponse({'ok': True})


@login_required
def dashboard_partial(request):
    context = {
        'resumo_mes': dashboard_selectors.obter_resumo_mes_atual(request.user),
        'ultimas_transacoes': dashboard_selectors.obter_ultimas_transacoes(
            request.user, limit=20
        ),
        'saldo': calculate_balance(request.user),
    }
    return render(
        request,
        'telegram_bot/fragmentos/dashboard_lancamentos.html',
        context,
    )
