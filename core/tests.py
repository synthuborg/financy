import pytest


class TestLandingPage:
    """Testes para a Landing Page."""

    def test_landing_page_retorna_200(self, client):
        """A URL raiz deve retornar HTTP 200 sem autenticação."""
        response = client.get('/')
        assert response.status_code == 200

    def test_landing_page_usa_template_correto(self, client):
        """Deve usar o template landing_page.html."""
        response = client.get('/')
        assert response.status_code == 200
        assert 'core/landing_page.html' in [t.name for t in response.templates]

    def test_landing_page_contem_link_login(self, client):
        """Deve conter link para o login."""
        response = client.get('/')
        assert b'/accounts/login/' in response.content

    def test_landing_page_contem_link_register(self, client):
        """Deve conter link para o cadastro."""
        response = client.get('/')
        assert b'/accounts/register/' in response.content

    def test_landing_page_contem_entradas(self, client):
        """Deve exibir o texto 'Entradas' (terminologia obrigatória)."""
        response = client.get('/')
        assert 'Entradas'.encode() in response.content

    def test_landing_page_contem_saidas(self, client):
        """Deve exibir o texto 'Saídas' (terminologia obrigatória)."""
        response = client.get('/')
        assert 'Saídas'.encode() in response.content
