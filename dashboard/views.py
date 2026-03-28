from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from . import selectors
from finances.services import calculate_balance
from finances import selectors as finances_selectors


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx['saldo'] = calculate_balance(user)
        ctx['resumo_mes'] = selectors.obter_resumo_mes_atual(user)
        ctx['ultimas_transacoes'] = selectors.obter_ultimas_transacoes(user)
        ctx['metas'] = selectors.obter_metas_resumo(user)
        ctx['budget_status'] = finances_selectors.get_budget_status(user)
        ctx['budget_alerts'] = finances_selectors.get_recent_budget_alerts(user)
        ctx['budget_calendar'] = finances_selectors.get_budget_calendar_data(user)
        return ctx


class GraficoEvolucaoView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/fragmentos/grafico_evolucao.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['dados'] = selectors.obter_dados_evolucao_6_meses(self.request.user)
        return ctx


class GraficoSaidasView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/fragmentos/grafico_saidas.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['dados'] = selectors.obter_distribuicao_saidas_mes(self.request.user)
        return ctx


class GraficoMetasView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/fragmentos/grafico_metas.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['dados'] = selectors.obter_dados_metas(self.request.user)
        return ctx


class GraficoInvestimentosView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/fragmentos/grafico_investimentos.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['dados'] = selectors.obter_dados_investimentos(self.request.user)
        return ctx
