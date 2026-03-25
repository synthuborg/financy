import pytest
from django.contrib.auth.models import User
from django.urls import reverse


class TestAdminPanelPermissoes:
    """Testa o controle de acesso ao admin_panel."""

    def test_anonimo_redirecionado(self, client):
        url = reverse('admin_panel:dashboard')
        response = client.get(url)
        assert response.status_code in [302, 403]

    def test_usuario_comum_recebe_403(self, client, usuario):
        client.login(username='testuser', password='testpass123')
        url = reverse('admin_panel:dashboard')
        response = client.get(url)
        assert response.status_code == 403

    def test_staff_acessa_dashboard(self, client, db):
        staff = User.objects.create_user(
            username='staffuser', password='staff123', is_staff=True
        )
        client.login(username='staffuser', password='staff123')
        url = reverse('admin_panel:dashboard')
        response = client.get(url)
        assert response.status_code == 200

    def test_staff_acessa_transaction_list(self, client, db):
        staff = User.objects.create_user(
            username='staffuser2', password='staff123', is_staff=True
        )
        client.login(username='staffuser2', password='staff123')
        url = reverse('admin_panel:transaction_list')
        response = client.get(url)
        assert response.status_code == 200

    def test_usuario_comum_recebe_403_em_transacoes(self, client, usuario):
        client.login(username='testuser', password='testpass123')
        url = reverse('admin_panel:transaction_list')
        response = client.get(url)
        assert response.status_code == 403
