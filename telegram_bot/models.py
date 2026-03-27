import base64
import hashlib
import hmac

# pylint: disable=no-member

from cryptography.fernet import Fernet
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class TelegramCredential(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='telegram_config',
    )
    token_hash = models.CharField(max_length=64, db_index=True)
    token_encrypted = models.TextField()
    chat_id_hash = models.CharField(max_length=64, unique=True)
    bot_username = models.CharField(max_length=100, blank=True)
    ativo = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Credencial Telegram'
        verbose_name_plural = 'Credenciais Telegram'

    def __str__(self):
        return f'Telegram de {self.user.username}'

    @staticmethod
    def _fernet():
        configured_key = getattr(settings, 'TELEGRAM_TOKEN_ENCRYPTION_KEY', '')
        if configured_key:
            key_bytes = configured_key.encode()
        else:
            digest = hashlib.sha256(settings.SECRET_KEY.encode()).digest()
            key_bytes = base64.urlsafe_b64encode(digest)
        return Fernet(key_bytes)

    @staticmethod
    def _hash_value(value: str) -> str:
        secret = getattr(settings, 'TELEGRAM_HASH_SECRET', settings.SECRET_KEY)
        return hmac.new(
            key=secret.encode(),
            msg=value.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()

    @classmethod
    def hash_chat_id(cls, chat_id: str) -> str:
        return cls._hash_value(str(chat_id))

    @classmethod
    def hash_token(cls, token: str) -> str:
        return cls._hash_value(token)

    def set_token(self, token: str) -> None:
        self.token_hash = self.hash_token(token)
        self.token_encrypted = self._fernet().encrypt(token.encode()).decode()

    def set_chat_id(self, chat_id: str) -> None:
        self.chat_id_hash = self.hash_chat_id(str(chat_id))

    def get_token(self) -> str:
        return self._fernet().decrypt(self.token_encrypted.encode()).decode()
