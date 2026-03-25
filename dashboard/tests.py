import pytest
from django.urls import reverse
from finances.models import Category, Transaction
from decimal import Decimal
from datetime import date


class TestDashboardHTTP:
    """Testa que as rotas do dashboard retornam HTTP 200."""

    def test_dashboard_requer_autenticacao(self, client):
        url = reverse('dashboard:dashboard')
        response = client.get(url)
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    def test_dashboard_autenticado_retorna_200(self, client_autenticado):
        url = reverse('dashboard:dashboard')
        response = client_autenticado.get(url)
        assert response.status_code == 200

    def test_grafico_evolucao_retorna_200(self, client_autenticado):
        url = reverse('dashboard:grafico_evolucao')
        response = client_autenticado.get(url)
        assert response.status_code == 200

    def test_grafico_saidas_retorna_200(self, client_autenticado):
        url = reverse('dashboard:grafico_saidas')
        response = client_autenticado.get(url)
        assert response.status_code == 200

    def test_grafico_metas_retorna_200(self, client_autenticado):
        url = reverse('dashboard:grafico_metas')
        response = client_autenticado.get(url)
        assert response.status_code == 200

    def test_grafico_investimentos_retorna_200(self, client_autenticado):
        url = reverse('dashboard:grafico_investimentos')
        response = client_autenticado.get(url)
        assert response.status_code == 200


class TestDashboardSelectors:
    """Testa os selectors do dashboard."""

    def test_evolucao_sem_transacoes(self, db, usuario):
        from dashboard.selectors import obter_dados_evolucao_6_meses
        dados = obter_dados_evolucao_6_meses(usuario)
        assert 'labels' in dados
        assert 'entradas' in dados
        assert 'saidas' in dados
        assert len(dados['labels']) == 6

    def test_distribuicao_saidas_sem_transacoes(self, db, usuario):
        from dashboard.selectors import obter_distribuicao_saidas_mes
        dados = obter_distribuicao_saidas_mes(usuario)
        assert 'labels' in dados
        assert 'valores' in dados
        assert dados['labels'] == []
        assert dados['valores'] == []

    def test_metas_retorna_dados_do_usuario(self, db, usuario):
        from dashboard.selectors import obter_dados_metas
        dados = obter_dados_metas(usuario)
        assert 'labels' in dados
        assert 'valores' in dados
        assert isinstance(dados['labels'], list)
        assert isinstance(dados['valores'], list)

    def test_investimentos_retorna_dados_mockados(self, db, usuario):
        from dashboard.selectors import obter_dados_investimentos
        dados = obter_dados_investimentos(usuario)
        assert 'labels' in dados
        assert 'valores' in dados
        assert len(dados['labels']) > 0

    def test_evolucao_com_transacoes(self, db, usuario):
        from dashboard.selectors import obter_dados_evolucao_6_meses
        categoria = Category.objects.create(
            nome='Salário', tipo='entrada', usuario=usuario
        )
        Transaction.objects.create(
            valor=Decimal('1000.00'),
            data=date.today(),
            tipo='entrada',
            descricao='Salário mensal',
            categoria=categoria,
            usuario=usuario
        )
        dados = obter_dados_evolucao_6_meses(usuario)
        assert sum(dados['entradas']) == 1000.0


class TestFinancesModels:
    """Testa os modelos do app finances."""

    def test_category_str(self, db, usuario):
        cat = Category.objects.create(
            nome='Alimentação', tipo='saida', usuario=usuario
        )
        assert str(cat) == 'Alimentação (Saída)'

    def test_transaction_str(self, db, usuario):
        cat = Category.objects.create(
            nome='Salário', tipo='entrada', usuario=usuario
        )
        t = Transaction.objects.create(
            valor=Decimal('500.00'),
            data=date.today(),
            tipo='entrada',
            descricao='Freelance',
            categoria=cat,
            usuario=usuario
        )
        assert 'Entrada' in str(t)
        assert 'Freelance' in str(t)

    def test_transaction_valor_invalido(self, db, usuario):
        from django.core.exceptions import ValidationError
        cat = Category.objects.create(
            nome='Teste', tipo='entrada', usuario=usuario
        )
        t = Transaction(
            valor=Decimal('-10.00'),
            data=date.today(),
            tipo='entrada',
            descricao='Inválido',
            categoria=cat,
            usuario=usuario
        )
        with pytest.raises(ValidationError):
            t.full_clean()

    def test_category_unique_per_user(self, db, usuario):
        from django.db import IntegrityError
        Category.objects.create(nome='Teste', tipo='entrada', usuario=usuario)
        with pytest.raises(IntegrityError):
            Category.objects.create(nome='Teste', tipo='entrada', usuario=usuario)


# ============================================================
# Fase 5 — Novos Seletores e Contexto do Dashboard
# ============================================================


@pytest.mark.django_db
class TestObterResumoMesAtual:

    def test_sem_transacoes_retorna_zeros(self, usuario):
        from dashboard.selectors import obter_resumo_mes_atual
        resultado = obter_resumo_mes_atual(usuario)
        assert resultado['total_entradas'] == Decimal('0')
        assert resultado['total_saidas'] == Decimal('0')
        assert resultado['saldo_liquido'] == Decimal('0')

    def test_contabiliza_entradas_do_mes(self, usuario):
        from dashboard.selectors import obter_resumo_mes_atual
        from finances.models import Transaction
        from django.utils import timezone
        hoje = timezone.now().date()
        Transaction.objects.create(
            usuario=usuario, valor='200.00',
            data=hoje, tipo='entrada', descricao='Salário'
        )
        resultado = obter_resumo_mes_atual(usuario)
        assert resultado['total_entradas'] == Decimal('200.00')

    def test_contabiliza_saidas_do_mes(self, usuario):
        from dashboard.selectors import obter_resumo_mes_atual
        from finances.models import Transaction
        from django.utils import timezone
        hoje = timezone.now().date()
        Transaction.objects.create(
            usuario=usuario, valor='50.00',
            data=hoje, tipo='saida', descricao='Aluguel'
        )
        resultado = obter_resumo_mes_atual(usuario)
        assert resultado['total_saidas'] == Decimal('50.00')

    def test_saldo_liquido_is_entradas_minus_saidas(self, usuario):
        from dashboard.selectors import obter_resumo_mes_atual
        from finances.models import Transaction
        from django.utils import timezone
        hoje = timezone.now().date()
        Transaction.objects.create(usuario=usuario, valor='300.00', data=hoje, tipo='entrada', descricao='E')
        Transaction.objects.create(usuario=usuario, valor='100.00', data=hoje, tipo='saida', descricao='S')
        resultado = obter_resumo_mes_atual(usuario)
        assert resultado['saldo_liquido'] == Decimal('200.00')

    def test_ignora_transacoes_de_outros_usuarios(self, usuario):
        from dashboard.selectors import obter_resumo_mes_atual
        from finances.models import Transaction
        from django.utils import timezone
        from django.contrib.auth.models import User
        hoje = timezone.now().date()
        outro = User.objects.create_user(username='outro_fase5', password='pass')
        Transaction.objects.create(usuario=outro, valor='999.00', data=hoje, tipo='entrada', descricao='X')
        resultado = obter_resumo_mes_atual(usuario)
        assert resultado['total_entradas'] == Decimal('0')


@pytest.mark.django_db
class TestObterUltimasTransacoes:

    def test_retorna_lista_vazia_sem_transacoes(self, usuario):
        from dashboard.selectors import obter_ultimas_transacoes
        resultado = list(obter_ultimas_transacoes(usuario))
        assert resultado == []

    def test_retorna_no_maximo_limit_transacoes(self, usuario):
        from dashboard.selectors import obter_ultimas_transacoes
        from finances.models import Transaction
        from django.utils import timezone
        hoje = timezone.now().date()
        for i in range(8):
            Transaction.objects.create(
                usuario=usuario, valor='10.00',
                data=hoje, tipo='saida', descricao=f'T{i}'
            )
        resultado = list(obter_ultimas_transacoes(usuario, limit=5))
        assert len(resultado) == 5

    def test_ordenado_por_data_decrescente(self, usuario):
        from dashboard.selectors import obter_ultimas_transacoes
        from finances.models import Transaction
        import datetime
        t1 = Transaction.objects.create(usuario=usuario, valor='1.00', data=datetime.date(2024, 1, 1), tipo='entrada', descricao='Antigo')
        t2 = Transaction.objects.create(usuario=usuario, valor='2.00', data=datetime.date(2024, 3, 1), tipo='entrada', descricao='Recente')
        resultado = list(obter_ultimas_transacoes(usuario, limit=2))
        assert resultado[0].pk == t2.pk


@pytest.mark.django_db
class TestDashboardViewComDados:

    def test_dashboard_200_autenticado(self, client_autenticado):
        from django.urls import reverse
        url = reverse('dashboard:dashboard')
        response = client_autenticado.get(url)
        assert response.status_code == 200

    def test_dashboard_contexto_tem_resumo_mes(self, client_autenticado):
        from django.urls import reverse
        url = reverse('dashboard:dashboard')
        response = client_autenticado.get(url)
        assert 'resumo_mes' in response.context

    def test_dashboard_contexto_tem_saldo(self, client_autenticado):
        from django.urls import reverse
        url = reverse('dashboard:dashboard')
        response = client_autenticado.get(url)
        assert 'saldo' in response.context

    def test_dashboard_contexto_tem_ultimas_transacoes(self, client_autenticado):
        from django.urls import reverse
        url = reverse('dashboard:dashboard')
        response = client_autenticado.get(url)
        assert 'ultimas_transacoes' in response.context


# ============================================================
# Fase 6 — Metas no Dashboard
# ============================================================


@pytest.mark.django_db
class TestObterMetasResumo:
    def test_sem_metas_retorna_lista_vazia(self, usuario):
        from dashboard.selectors import obter_metas_resumo
        resultado = obter_metas_resumo(usuario)
        assert resultado == []

    def test_retorna_no_maximo_limit(self, usuario):
        from dashboard.selectors import obter_metas_resumo
        from finances.models import Goal
        for i in range(5):
            Goal.objects.create(usuario=usuario, titulo=f'Meta {i}', valor_alvo='100.00')
        resultado = obter_metas_resumo(usuario, limit=3)
        assert len(resultado) == 3

    def test_dashboard_contexto_tem_metas(self, client_autenticado):
        from django.urls import reverse
        response = client_autenticado.get(reverse('dashboard:dashboard'))
        assert 'metas' in response.context
