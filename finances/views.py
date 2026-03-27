import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView

from . import selectors
from . import selectors as finances_selectors
from .forms import (
    AccountForm,
    CategoryForm,
    GoalAddProgressForm,
    GoalForm,
    ImportStatementForm,
    ReportFilterForm,
    TransactionForm,
)
from .models import Account, Category, Goal, Transaction
from .services import (
    add_progress_to_goal,
    create_goal,
    create_transaction,
    delete_goal,
    delete_transaction,
    generate_excel_report,
    generate_pdf_report,
    process_bank_statement_import,
    update_goal,
    update_transaction,
)


# ---------------------------------------------------------------------------
# Transações
# ---------------------------------------------------------------------------

class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'finances/transaction_list.html'
    context_object_name = 'transacoes'
    paginate_by = 20

    def get_queryset(self):
        qs = selectors.get_all_transactions(self.request.user)
        tipo = self.request.GET.get('tipo')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        descricao = self.request.GET.get('q')

        if tipo in ('entrada', 'saida'):
            qs = qs.filter(tipo=tipo)
        if data_inicio:
            qs = qs.filter(data__gte=data_inicio)
        if data_fim:
            qs = qs.filter(data__lte=data_fim)
        if descricao:
            qs = qs.filter(descricao__icontains=descricao)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filtros'] = {
            'tipo': self.request.GET.get('tipo', ''),
            'data_inicio': self.request.GET.get('data_inicio', ''),
            'data_fim': self.request.GET.get('data_fim', ''),
            'q': self.request.GET.get('q', ''),
        }
        ctx['import_form'] = ImportStatementForm(user=self.request.user)
        return ctx


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finances/transaction_form.html'
    success_url = reverse_lazy('finances:transaction_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        if data.get('categoria'):
            data['categoria_id'] = data.pop('categoria').pk
        else:
            data.pop('categoria', None)
        if data.get('conta'):
            data['conta_id'] = data.pop('conta').pk
        else:
            data.pop('conta', None)

        try:
            create_transaction(self.request.user, data)
            messages.success(self.request, 'Transação criada com sucesso!')
            return redirect(self.success_url)
        except Exception as exc:
            messages.error(self.request, f'Erro ao criar transação: {exc}')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nova Transação'
        ctx['btn_label'] = 'Criar Transação'
        return ctx


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finances/transaction_form.html'
    success_url = reverse_lazy('finances:transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        if data.get('categoria'):
            data['categoria_id'] = data.pop('categoria').pk
        else:
            data.pop('categoria', None)
        if data.get('conta'):
            data['conta_id'] = data.pop('conta').pk
        else:
            data.pop('conta', None)

        try:
            update_transaction(self.object.pk, self.request.user, data)
            messages.success(self.request, 'Transação atualizada com sucesso!')
            return redirect(self.success_url)
        except Exception as exc:
            messages.error(self.request, f'Erro ao atualizar transação: {exc}')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar Transação'
        ctx['btn_label'] = 'Salvar Alterações'
        return ctx


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'finances/transaction_confirm_delete.html'
    success_url = reverse_lazy('finances:transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        try:
            delete_transaction(self.object.pk, self.request.user)
            messages.success(self.request, 'Transação excluída com sucesso!')
        except Exception as exc:
            messages.error(self.request, f'Erro ao excluir: {exc}')
        return redirect(self.success_url)


# ---------------------------------------------------------------------------
# Categorias
# ---------------------------------------------------------------------------

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'finances/category_list.html'
    context_object_name = 'categorias'

    def get_queryset(self):
        return Category.objects.filter(usuario=self.request.user).order_by('nome')


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'finances/category_form.html'
    success_url = reverse_lazy('finances:category_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Categoria criada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nova Categoria'
        ctx['btn_label'] = 'Criar Categoria'
        return ctx


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'finances/category_form.html'
    success_url = reverse_lazy('finances:category_list')

    def get_queryset(self):
        return Category.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Categoria atualizada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar Categoria'
        ctx['btn_label'] = 'Salvar Alterações'
        return ctx


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'finances/category_confirm_delete.html'
    success_url = reverse_lazy('finances:category_list')

    def get_queryset(self):
        return Category.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Categoria excluída!')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Contas
# ---------------------------------------------------------------------------

class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'finances/account_list.html'
    context_object_name = 'contas'

    def get_queryset(self):
        return Account.objects.filter(usuario=self.request.user).order_by('nome')


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'finances/account_form.html'
    success_url = reverse_lazy('finances:account_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Conta criada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nova Conta'
        ctx['btn_label'] = 'Criar Conta'
        return ctx


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'finances/account_form.html'
    success_url = reverse_lazy('finances:account_list')

    def get_queryset(self):
        return Account.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Conta atualizada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar Conta'
        ctx['btn_label'] = 'Salvar Alterações'
        return ctx


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'finances/account_confirm_delete.html'
    success_url = reverse_lazy('finances:account_list')

    def get_queryset(self):
        return Account.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'Conta excluída!')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Contas Correntes (conta_corrente + carteira)
# ---------------------------------------------------------------------------

class ContaCorrenteListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'finances/conta_corrente_list.html'
    context_object_name = 'contas'

    def get_queryset(self):
        return Account.objects.filter(
            usuario=self.request.user,
            tipo__in=['conta_corrente', 'carteira'],
        ).order_by('nome')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['contas_com_saldo'] = [
            (
                conta,
                selectors.get_account_balance(conta.pk, self.request.user),
                selectors.get_transactions_by_account(conta.pk, self.request.user),
            )
            for conta in ctx['contas']
        ]
        return ctx


class ContaCorrenteCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'finances/account_form.html'
    success_url = reverse_lazy('finances:conta_corrente_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tipo'].choices = [
            ('conta_corrente', 'Conta Corrente'),
            ('carteira', 'Carteira'),
        ]
        return form

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Conta corrente criada com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nova Conta Corrente'
        ctx['btn_label'] = 'Criar Conta'
        return ctx


class ContaCorrenteUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'finances/account_form.html'
    success_url = reverse_lazy('finances:conta_corrente_list')

    def get_queryset(self):
        return Account.objects.filter(
            usuario=self.request.user,
            tipo__in=['conta_corrente', 'carteira'],
        )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tipo'].choices = [
            ('conta_corrente', 'Conta Corrente'),
            ('carteira', 'Carteira'),
        ]
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Conta corrente atualizada!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar Conta Corrente'
        ctx['btn_label'] = 'Salvar Alterações'
        return ctx


class ContaCorrenteDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'finances/account_confirm_delete.html'
    success_url = reverse_lazy('finances:conta_corrente_list')

    def get_queryset(self):
        return Account.objects.filter(
            usuario=self.request.user,
            tipo__in=['conta_corrente', 'carteira'],
        )

    def form_valid(self, form):
        messages.success(self.request, 'Conta excluída!')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Cartões de Crédito
# ---------------------------------------------------------------------------

class CartaoCreditoListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'finances/cartao_credito_list.html'
    context_object_name = 'cartoes'

    def get_queryset(self):
        return Account.objects.filter(
            usuario=self.request.user,
            tipo='cartao_credito',
        ).order_by('nome')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['cartoes_com_fatura'] = [
            (cartao, selectors.get_account_balance(cartao.pk, self.request.user))
            for cartao in ctx['cartoes']
        ]
        return ctx


class CartaoCreditoCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'finances/account_form.html'
    success_url = reverse_lazy('finances:cartao_credito_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tipo'].choices = [('cartao_credito', 'Cartão de Crédito')]
        return form

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.tipo = 'cartao_credito'
        messages.success(self.request, 'Cartão de crédito criado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Novo Cartão de Crédito'
        ctx['btn_label'] = 'Criar Cartão'
        return ctx


class CartaoCreditoUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'finances/account_form.html'
    success_url = reverse_lazy('finances:cartao_credito_list')

    def get_queryset(self):
        return Account.objects.filter(
            usuario=self.request.user,
            tipo='cartao_credito',
        )

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['tipo'].choices = [('cartao_credito', 'Cartão de Crédito')]
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Cartão atualizado!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar Cartão de Crédito'
        ctx['btn_label'] = 'Salvar Alterações'
        return ctx


class CartaoCreditoDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'finances/account_confirm_delete.html'
    success_url = reverse_lazy('finances:cartao_credito_list')

    def get_queryset(self):
        return Account.objects.filter(
            usuario=self.request.user,
            tipo='cartao_credito',
        )

    def form_valid(self, form):
        messages.success(self.request, 'Cartão excluído!')
        return super().form_valid(form)


# ---------------------------------------------------------------------------
# Metas
# ---------------------------------------------------------------------------

class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    template_name = 'finances/goal_list.html'
    context_object_name = 'metas'

    def get_queryset(self):
        return finances_selectors.get_all_goals(self.request.user)


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = 'finances/goal_form.html'
    success_url = reverse_lazy('finances:goal_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        if data.get('categoria'):
            data['categoria_id'] = data.pop('categoria').pk
        else:
            data.pop('categoria', None)
        try:
            create_goal(self.request.user, data)
            messages.success(self.request, 'Meta criada com sucesso!')
            return redirect(self.success_url)
        except Exception as exc:
            messages.error(self.request, f'Erro: {exc}')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Nova Meta'
        ctx['btn_label'] = 'Criar Meta'
        return ctx


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    form_class = GoalForm
    template_name = 'finances/goal_form.html'
    success_url = reverse_lazy('finances:goal_list')

    def get_queryset(self):
        return Goal.objects.filter(usuario=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        data = form.cleaned_data.copy()
        if data.get('categoria'):
            data['categoria_id'] = data.pop('categoria').pk
        else:
            data.pop('categoria', None)
        try:
            update_goal(self.object.pk, self.request.user, data)
            messages.success(self.request, 'Meta atualizada com sucesso!')
            return redirect(self.success_url)
        except Exception as exc:
            messages.error(self.request, f'Erro: {exc}')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Editar Meta'
        ctx['btn_label'] = 'Salvar Alterações'
        return ctx


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal
    template_name = 'finances/goal_confirm_delete.html'
    success_url = reverse_lazy('finances:goal_list')

    def get_queryset(self):
        return Goal.objects.filter(usuario=self.request.user)

    def form_valid(self, form):
        try:
            delete_goal(self.object.pk, self.request.user)
            messages.success(self.request, 'Meta excluída!')
        except Exception as exc:
            messages.error(self.request, f'Erro ao excluir: {exc}')
        return redirect(self.success_url)


class GoalAddProgressView(LoginRequiredMixin, View):
    def post(self, request, pk):
        form = GoalAddProgressForm(request.POST)
        if form.is_valid():
            try:
                add_progress_to_goal(pk, request.user, form.cleaned_data['valor'])
                messages.success(request, 'Progresso adicionado!')
            except Exception as exc:
                messages.error(request, f'Erro: {exc}')
        else:
            messages.error(request, 'Valor inválido.')
        return redirect('finances:goal_list')


# ---------------------------------------------------------------------------
# Importação de Extratos
# ---------------------------------------------------------------------------

class ImportStatementView(LoginRequiredMixin, View):
    def post(self, request):
        form = ImportStatementForm(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            arquivo = form.cleaned_data['arquivo']
            conta = form.cleaned_data['conta']
            try:
                result = process_bank_statement_import(arquivo, request.user, conta)
                if result['criadas']:
                    messages.success(
                        request,
                        f'{result["criadas"]} transações importadas com sucesso!',
                    )
                if result['ignoradas']:
                    messages.info(
                        request,
                        f'{result["ignoradas"]} transações ignoradas (duplicadas).',
                    )
                if result['erros']:
                    messages.warning(
                        request,
                        f'Erros durante importação: {", ".join(result["erros"])}',
                    )
            except Exception as exc:
                messages.error(request, f'Erro ao importar extrato: {exc}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
        return redirect('finances:transaction_list')


# ---------------------------------------------------------------------------
# Relatórios
# ---------------------------------------------------------------------------

class ReportView(LoginRequiredMixin, FormView):
    template_name = 'finances/report_form.html'
    form_class = ReportFilterForm

    def get_initial(self):
        hoje = datetime.date.today()
        return {
            'data_inicio': hoje.replace(day=1),
            'data_fim': hoje,
            'formato': 'pdf',
        }

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = ctx.get('form')
        inicial = self.get_initial()

        data_inicio = inicial['data_inicio']
        data_fim = inicial['data_fim']

        if getattr(form, 'is_bound', False):
            data_inicio = form.cleaned_data.get('data_inicio') or data_inicio
            data_fim = form.cleaned_data.get('data_fim') or data_fim

        ctx['report_preview'] = finances_selectors.get_report_data(
            self.request.user,
            data_inicio,
            data_fim,
        )
        ctx['formatos_disponiveis'] = dict(form.fields['formato'].choices)
        return ctx

    def form_valid(self, form):
        data_inicio = form.cleaned_data['data_inicio']
        data_fim = form.cleaned_data['data_fim']
        formato = form.cleaned_data['formato']
        user = self.request.user

        if formato == 'pdf':
            content = generate_pdf_report(user, data_inicio, data_fim)
            response = HttpResponse(
                content, content_type='application/pdf',
            )
            response['Content-Disposition'] = (
                f'attachment; filename="relatorio_{data_inicio}_{data_fim}.pdf"'
            )
        else:
            content = generate_excel_report(user, data_inicio, data_fim)
            response = HttpResponse(
                content,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
            response['Content-Disposition'] = (
                f'attachment; filename="relatorio_{data_inicio}_{data_fim}.xlsx"'
            )
        return response
