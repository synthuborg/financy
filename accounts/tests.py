import pytest
from django.urls import reverse
from django.contrib.auth.models import User


class TestAutenticacaoHTTP:
    """Testa status HTTP das rotas de autenticação."""

    def test_login_retorna_200(self, client):
        url = reverse('accounts:login')
        response = client.get(url)
        assert response.status_code == 200

    def test_register_retorna_200(self, client):
        url = reverse('accounts:register')
        response = client.get(url)
        assert response.status_code == 200

    def test_logout_redireciona(self, client_autenticado):
        url = reverse('accounts:logout')
        response = client_autenticado.post(url)
        assert response.status_code in [200, 302]

    def test_login_usa_template_correto(self, client):
        url = reverse('accounts:login')
        response = client.get(url)
        assert 'accounts/login.html' in [t.name for t in response.templates]

    def test_register_usa_template_correto(self, client):
        url = reverse('accounts:register')
        response = client.get(url)
        assert 'accounts/register.html' in [t.name for t in response.templates]


class TestRegistro:
    """Testa o fluxo de registro de usuário."""

    def test_registro_cria_usuario(self, client, db):
        url = reverse('accounts:register')
        data = {
            'username': 'novousuario',
            'password1': 'SenhaForte@2026',
            'password2': 'SenhaForte@2026',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert User.objects.filter(username='novousuario').exists()

    def test_registro_redireciona_para_login(self, client, db):
        url = reverse('accounts:register')
        data = {
            'username': 'outronome',
            'password1': 'SenhaForte@2026',
            'password2': 'SenhaForte@2026',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    def test_registro_senha_fraca_falha(self, client, db):
        url = reverse('accounts:register')
        data = {
            'username': 'testuser2',
            'password1': '123',
            'password2': '123',
        }
        response = client.post(url, data)
        assert response.status_code == 200  # Volta ao form com erro


class TestLogin:
    """Testa o fluxo de login."""

    def test_login_valido_redireciona_para_dashboard(self, client, usuario):
        url = reverse('accounts:login')
        data = {
            'username': 'testuser',
            'password': 'testpass123',
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert '/dashboard/' in response['Location']

    def test_login_invalido_retorna_erro(self, client, db):
        url = reverse('accounts:login')
        data = {
            'username': 'naoexiste',
            'password': 'senhaerrada',
        }
        response = client.post(url, data)
        assert response.status_code == 200  # Volta ao form com erro
