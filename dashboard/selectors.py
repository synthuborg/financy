import calendar
from decimal import Decimal

from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from finances.models import Transaction


def obter_dados_evolucao_6_meses(user):
    """Retorna dados de Entradas e Saídas agrupados por mês (últimos 6 meses)."""
    hoje = timezone.now().date()
    mes = hoje.month - 5
    ano = hoje.year
    if mes <= 0:
        mes += 12
        ano -= 1
    seis_meses_atras = hoje.replace(year=ano, month=mes, day=1)

    entradas = (
        Transaction.objects.filter(
            usuario=user,
            tipo='entrada',
            data__gte=seis_meses_atras,
        )
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(total=Sum('valor'))
        .order_by('mes')
    )

    saidas = (
        Transaction.objects.filter(
            usuario=user,
            tipo='saida',
            data__gte=seis_meses_atras,
        )
        .annotate(mes=TruncMonth('data'))
        .values('mes')
        .annotate(total=Sum('valor'))
        .order_by('mes')
    )

    meses_map_entradas = {
        e['mes'].strftime('%Y-%m'): float(e['total']) for e in entradas
    }
    meses_map_saidas = {
        s['mes'].strftime('%Y-%m'): float(s['total']) for s in saidas
    }

    meses_labels = []
    dados_entradas = []
    dados_saidas = []

    for i in range(6):
        mes_ref = hoje.month - 5 + i
        ano_ref = hoje.year
        if mes_ref <= 0:
            mes_ref += 12
            ano_ref -= 1
        elif mes_ref > 12:
            mes_ref -= 12
            ano_ref += 1
        chave = f'{ano_ref:04d}-{mes_ref:02d}'
        nome_mes = calendar.month_abbr[mes_ref]
        meses_labels.append(nome_mes)
        dados_entradas.append(meses_map_entradas.get(chave, 0))
        dados_saidas.append(meses_map_saidas.get(chave, 0))

    return {
        'labels': meses_labels,
        'entradas': dados_entradas,
        'saidas': dados_saidas,
    }


def obter_distribuicao_saidas_mes(user):
    """Retorna total de Saídas do mês atual agrupadas por categoria."""
    hoje = timezone.now().date()
    inicio_mes = hoje.replace(day=1)

    saidas_por_categoria = (
        Transaction.objects.filter(
            usuario=user,
            tipo='saida',
            data__gte=inicio_mes,
            data__lte=hoje,
        )
        .values('categoria__nome')
        .annotate(total=Sum('valor'))
        .order_by('-total')
    )

    labels = []
    valores = []
    for item in saidas_por_categoria:
        labels.append(item['categoria__nome'] or 'Sem Categoria')
        valores.append(float(item['total']))

    return {
        'labels': labels,
        'valores': valores,
    }


def obter_dados_metas(user):
    """Retorna percentual de conclusão das metas do usuário."""
    from finances.models import Goal
    metas = Goal.objects.filter(usuario=user).order_by('titulo')[:5]
    labels = [m.titulo for m in metas]
    valores = [m.percentual_concluido for m in metas]
    return {
        'labels': labels,
        'valores': valores,
    }


def obter_dados_investimentos(user):
    """Retorna dados mockados de investimentos."""
    return {
        'labels': ['Renda Fixa', 'Ações', 'FIIs', 'Cripto'],
        'valores': [50, 25, 15, 10],
    }


def obter_resumo_mes_atual(user):
    """Retorna totais de Entradas, Saídas e Saldo Líquido do mês corrente."""
    from finances.models import Transaction
    hoje = timezone.now().date()
    inicio_mes = hoje.replace(day=1)

    totais = (
        Transaction.objects
        .filter(usuario=user, data__gte=inicio_mes)
        .values('tipo')
        .annotate(total=Sum('valor'))
    )
    resultado = {'total_entradas': Decimal('0'), 'total_saidas': Decimal('0')}
    for item in totais:
        if item['tipo'] == 'entrada':
            resultado['total_entradas'] = item['total'] or Decimal('0')
        elif item['tipo'] == 'saida':
            resultado['total_saidas'] = item['total'] or Decimal('0')
    resultado['saldo_liquido'] = resultado['total_entradas'] - resultado['total_saidas']
    return resultado


def obter_ultimas_transacoes(user, limit=5):
    """Retorna as últimas `limit` transações do usuário."""
    from finances.models import Transaction
    return (
        Transaction.objects
        .filter(usuario=user)
        .select_related('categoria', 'conta')
        .order_by('-data', '-pk')[:limit]
    )


def obter_metas_resumo(user, limit=3):
    """Retorna as primeiras `limit` metas do usuário ordenadas por prazo."""
    from finances.models import Goal
    return list(
        Goal.objects.filter(usuario=user)
        .select_related('categoria')
        .order_by('prazo', 'titulo')[:limit]
    )
