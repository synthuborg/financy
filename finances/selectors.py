# Consultas otimizadas - Read operations
from decimal import Decimal

from django.db.models import Sum
from django.shortcuts import get_object_or_404

from .models import Account, Transaction


def get_account_balance(account_id: int, user) -> Decimal:
    """
    Calcula o saldo de uma conta específica do usuário.
    - Conta Corrente / Carteira: sum(entradas) - sum(saídas)
    - Cartão de Crédito: sum(saídas) — representa a fatura atual
    Levanta Http404 se a conta não existir ou não pertencer ao usuário.
    """
    conta = get_object_or_404(Account, pk=account_id, usuario=user)
    qs = Transaction.objects.filter(conta=conta, usuario=user)
    entradas = qs.filter(tipo='entrada').aggregate(total=Sum('valor'))['total'] or Decimal('0')
    saidas = qs.filter(tipo='saida').aggregate(total=Sum('valor'))['total'] or Decimal('0')
    if conta.tipo == 'cartao_credito':
        return saidas
    return entradas - saidas


def get_all_transactions(user):
    """
    Retorna todas as transações do usuário ordenadas por data decrescente.
    Usa select_related para evitar N+1 queries.
    """
    return (
        Transaction.objects
        .filter(usuario=user)
        .select_related('categoria', 'conta')
        .order_by('-data', '-pk')
    )


def get_transaction_by_id(transaction_id: int, user):
    """
    Busca uma transação pelo ID com escopo do usuário.
    Levanta Http404 se não encontrar ou não pertencer ao usuário.
    """
    return get_object_or_404(
        Transaction.objects.select_related('categoria', 'conta'),
        pk=transaction_id,
        usuario=user,
    )


def get_all_goals(user):
    """Retorna todas as metas do usuário ordenadas por prazo."""
    from .models import Goal
    return Goal.objects.filter(usuario=user).select_related('categoria')


def get_transactions_by_account(account_id: int, user, limit: int = 5):
    """Retorna as últimas transações de uma conta específica do usuário."""
    return (
        Transaction.objects
        .filter(conta_id=account_id, usuario=user)
        .select_related('categoria', 'conta')
        .order_by('-data', '-pk')[:limit]
    )


def get_goal_by_id(goal_id: int, user):
    """Retorna uma meta específica do usuário ou 404."""
    from .models import Goal
    return get_object_or_404(Goal.objects.select_related('categoria'), pk=goal_id, usuario=user)


def get_report_data(user, data_inicio, data_fim):
    """
    Agrega todos os dados necessários para gerar relatório financeiro.
    Retorna dict com: resumo, transações, distribuição por categoria.
    """
    from django.db.models import Max

    qs = Transaction.objects.filter(
        usuario=user,
        data__gte=data_inicio,
        data__lte=data_fim,
    ).select_related('categoria', 'conta')

    total_entradas = (
        qs.filter(tipo='entrada')
        .aggregate(total=Sum('valor'))['total']
        or Decimal('0.00')
    )
    total_saidas = (
        qs.filter(tipo='saida')
        .aggregate(total=Sum('valor'))['total']
        or Decimal('0.00')
    )
    maior_entrada = (
        qs.filter(tipo='entrada')
        .aggregate(maior=Max('valor'))['maior']
    )
    maior_saida = (
        qs.filter(tipo='saida')
        .aggregate(maior=Max('valor'))['maior']
    )

    # Distribuição por categoria (somente saídas)
    from django.db.models import Count
    cat_qs = (
        qs.filter(tipo='saida', categoria__isnull=False)
        .values('categoria__nome')
        .annotate(total=Sum('valor'))
        .order_by('-total')
    )
    por_categoria = []
    for item in cat_qs:
        percentual = (
            float(item['total'] / total_saidas * 100)
            if total_saidas > 0
            else 0.0
        )
        por_categoria.append({
            'categoria': item['categoria__nome'],
            'total': item['total'],
            'percentual': round(percentual, 2),
        })

    return {
        'periodo': {'inicio': data_inicio, 'fim': data_fim},
        'resumo': {
            'total_entradas': total_entradas,
            'total_saidas': total_saidas,
            'saldo_liquido': total_entradas - total_saidas,
            'num_transacoes': qs.count(),
            'maior_entrada': maior_entrada,
            'maior_saida': maior_saida,
        },
        'transacoes': qs.order_by('-data', '-pk'),
        'por_categoria': por_categoria,
    }
