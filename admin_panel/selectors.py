from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum
from django.db.models.functions import Coalesce

from finances.models import Account, Category, Transaction


def get_admin_dashboard_stats():
    """Returns dict with global KPI stats for the admin dashboard."""
    totals = Transaction.objects.aggregate(
        total_entradas=Coalesce(
            Sum('valor', filter=Q(tipo='entrada')),
            Decimal('0'),
        ),
        total_saidas=Coalesce(
            Sum('valor', filter=Q(tipo='saida')),
            Decimal('0'),
        ),
    )
    return {
        'total_usuarios': User.objects.count(),
        'total_transacoes': Transaction.objects.count(),
        'total_entradas': totals['total_entradas'],
        'total_saidas': totals['total_saidas'],
        'saldo_global': totals['total_entradas'] - totals['total_saidas'],
        'total_categorias': Category.objects.count(),
        'total_contas': Account.objects.count(),
    }


def get_all_users_with_stats():
    """Returns queryset of all Users annotated with transaction stats."""
    return (
        User.objects
        .annotate(
            num_transacoes=Count('transacoes'),
            total_entradas=Coalesce(
                Sum('transacoes__valor', filter=Q(transacoes__tipo='entrada')),
                Decimal('0'),
            ),
            total_saidas=Coalesce(
                Sum('transacoes__valor', filter=Q(transacoes__tipo='saida')),
                Decimal('0'),
            ),
        )
        .order_by('username')
    )


def get_admin_transactions(filters=None):
    """Returns all transactions with select_related, optionally filtered."""
    qs = (
        Transaction.objects
        .select_related('categoria', 'conta', 'usuario')
        .order_by('-data', '-pk')
    )
    if not filters:
        return qs

    if filters.get('user'):
        qs = qs.filter(usuario_id=filters['user'])
    if filters.get('tipo'):
        qs = qs.filter(tipo=filters['tipo'])
    if filters.get('data_inicio'):
        qs = qs.filter(data__gte=filters['data_inicio'])
    if filters.get('data_fim'):
        qs = qs.filter(data__lte=filters['data_fim'])
    if filters.get('q'):
        qs = qs.filter(descricao__icontains=filters['q'])

    return qs


def get_admin_categories():
    """Returns all categories with select_related, ordered by nome."""
    return (
        Category.objects
        .select_related('usuario')
        .order_by('nome')
    )
