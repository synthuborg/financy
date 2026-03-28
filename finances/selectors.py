# Consultas otimizadas - Read operations
import calendar
import datetime
from decimal import Decimal

from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404

from .models import Account, BudgetAlertEvent, MonthlyBudgetConfig, Transaction


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


def get_monthly_budget_config(user):
    return MonthlyBudgetConfig.objects.filter(usuario=user).first()


def get_budget_status(user, reference_date=None):
    config = get_monthly_budget_config(user)
    if config is None:
        return None

    base_date = reference_date or datetime.date.today()
    limite_mensal = config.limite_mensal

    total_saidas = (
        Transaction.objects.filter(
            usuario=user,
            tipo='saida',
            data__year=base_date.year,
            data__month=base_date.month,
        ).aggregate(total=Sum('valor'))['total']
        or Decimal('0.00')
    )

    restante = limite_mensal - total_saidas
    consumo_percentual = (
        (total_saidas / limite_mensal) * Decimal('100')
        if limite_mensal > 0 else Decimal('0.00')
    )
    restante_percentual = (
        max((restante / limite_mensal) * Decimal('100'), Decimal('0.00'))
        if limite_mensal > 0 else Decimal('0.00')
    )

    ultimo_dia = calendar.monthrange(base_date.year, base_date.month)[1]
    dias_restantes = (
        datetime.date(base_date.year, base_date.month, ultimo_dia) - base_date
    ).days + 1
    limite_diario_recomendado = (
        (max(restante, Decimal('0.00')) / Decimal(str(dias_restantes))).quantize(Decimal('0.01'))
        if dias_restantes > 0 else Decimal('0.00')
    )

    if consumo_percentual >= Decimal('100'):
        nivel_alerta = 'danger'
        mensagem = 'Limite mensal atingido ou ultrapassado.'
    elif consumo_percentual >= Decimal('90'):
        nivel_alerta = 'warning-10'
        mensagem = 'Atenção: faltam menos de 10% para o limite mensal.'
    elif consumo_percentual >= Decimal('80'):
        nivel_alerta = 'warning-20'
        mensagem = 'Atenção: faltam menos de 20% para o limite mensal.'
    else:
        nivel_alerta = 'ok'
        mensagem = 'Consumo dentro da meta de orçamento.'

    return {
        'config': config,
        'ano': base_date.year,
        'mes': base_date.month,
        'limite_mensal': limite_mensal,
        'total_saidas': total_saidas,
        'restante': restante,
        'consumo_percentual': consumo_percentual.quantize(Decimal('0.01')),
        'restante_percentual': restante_percentual.quantize(Decimal('0.01')),
        'limite_diario_recomendado': limite_diario_recomendado,
        'nivel_alerta': nivel_alerta,
        'mensagem': mensagem,
    }


def get_budget_calendar_data(user, reference_date=None):
    status = get_budget_status(user, reference_date=reference_date)
    if status is None:
        return None

    base_date = reference_date or datetime.date.today()
    year = base_date.year
    month = base_date.month
    limite_mensal = status['limite_mensal']

    saidas_por_dia = {
        item['data']: {
            'total': item['total'] or Decimal('0.00'),
            'quantidade': item['quantidade'] or 0,
        }
        for item in (
            Transaction.objects.filter(
                usuario=user,
                tipo='saida',
                data__year=year,
                data__month=month,
            ).values('data').annotate(total=Sum('valor'), quantidade=Count('id'))
        )
    }

    total_dias = calendar.monthrange(year, month)[1]
    linhas = []
    cumulativo = Decimal('0.00')

    for week in calendar.Calendar(firstweekday=6).monthdayscalendar(year, month):
        linha = []
        for day in week:
            if day == 0:
                linha.append(None)
                continue

            data_ref = datetime.date(year, month, day)
            dados_dia = saidas_por_dia.get(
                data_ref,
                {'total': Decimal('0.00'), 'quantidade': 0},
            )
            gasto_dia = Decimal(str(dados_dia['total']))
            qtd_despesas = int(dados_dia['quantidade'])

            dias_restantes_incluindo = total_dias - day + 1
            limite_recomendado_dia = (
                (
                    max(limite_mensal - cumulativo, Decimal('0.00'))
                    / Decimal(str(dias_restantes_incluindo))
                ).quantize(Decimal('0.01'))
                if dias_restantes_incluindo > 0 else Decimal('0.00')
            )

            percentual_dia = (
                ((gasto_dia / limite_mensal) * Decimal('100')).quantize(Decimal('0.01'))
                if limite_mensal > 0 else Decimal('0.00')
            )

            cumulativo += gasto_dia

            linha.append({
                'dia': day,
                'data': data_ref,
                'gasto_dia': gasto_dia,
                'qtd_despesas': qtd_despesas,
                'percentual_dia': percentual_dia,
                'limite_recomendado_dia': limite_recomendado_dia,
                'is_today': data_ref == datetime.date.today(),
            })
        linhas.append(linha)

    return {
        'ano': year,
        'mes': month,
        'mes_nome': calendar.month_name[month],
        'linhas': linhas,
    }


def get_recent_budget_alerts(user, reference_date=None, limit=5):
    base_date = reference_date or datetime.date.today()
    return list(
        BudgetAlertEvent.objects.filter(
            usuario=user,
            ano=base_date.year,
            mes=base_date.month,
        ).order_by('-criado_em')[:limit]
    )
