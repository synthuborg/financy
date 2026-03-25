import pytest
from django.contrib.auth.models import User


@pytest.fixture
def usuario(db):
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )


@pytest.fixture
def client_autenticado(client, usuario):
    client.login(username='testuser', password='testpass123')
    return client
