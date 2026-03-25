from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import DeleteView, ListView, TemplateView

from finances.models import Category, Transaction

from .selectors import (
    get_admin_categories,
    get_admin_dashboard_stats,
    get_admin_transactions,
    get_all_users_with_stats,
)


class StaffRequiredMixin(UserPassesTestMixin):
    """Garante que apenas usuários is_staff têm acesso."""

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class AdminDashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'admin_panel/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update(get_admin_dashboard_stats())
        return ctx


class AdminUserListView(StaffRequiredMixin, ListView):
    template_name = 'admin_panel/user_list.html'
    context_object_name = 'usuarios'
    paginate_by = 50

    def get_queryset(self):
        return get_all_users_with_stats()


class AdminUserToggleView(StaffRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)

        if user == request.user:
            messages.error(
                request,
                'Você não pode desativar sua própria conta.',
            )
            return redirect('admin_panel:user_list')

        if user.is_superuser:
            messages.error(
                request,
                'Não é permitido alterar o status de um superusuário.',
            )
            return redirect('admin_panel:user_list')

        user.is_active = not user.is_active
        user.save(update_fields=['is_active'])
        status = 'ativado' if user.is_active else 'desativado'
        messages.success(
            request,
            f'Usuário {user.username} foi {status} com sucesso.',
        )
        return redirect('admin_panel:user_list')


class AdminTransactionListView(StaffRequiredMixin, ListView):
    model = Transaction
    template_name = 'admin_panel/transaction_list.html'
    context_object_name = 'transacoes'
    paginate_by = 50

    def get_queryset(self):
        filters = {
            'user': self.request.GET.get('user'),
            'tipo': self.request.GET.get('tipo'),
            'data_inicio': self.request.GET.get('data_inicio'),
            'data_fim': self.request.GET.get('data_fim'),
            'q': self.request.GET.get('q'),
        }
        filters = {k: v for k, v in filters.items() if v}
        return get_admin_transactions(filters or None)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filtros'] = {
            'user': self.request.GET.get('user', ''),
            'tipo': self.request.GET.get('tipo', ''),
            'data_inicio': self.request.GET.get('data_inicio', ''),
            'data_fim': self.request.GET.get('data_fim', ''),
            'q': self.request.GET.get('q', ''),
        }
        ctx['usuarios'] = User.objects.order_by('username')
        return ctx


class AdminTransactionDeleteView(StaffRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'admin_panel/transaction_confirm_delete.html'
    context_object_name = 'transacao'

    def get_success_url(self):
        messages.success(self.request, 'Transação excluída com sucesso.')
        return self.request.META.get(
            'HTTP_REFERER',
            '/admin-panel/transacoes/',
        )


class AdminCategoryListView(StaffRequiredMixin, ListView):
    template_name = 'admin_panel/category_list.html'
    context_object_name = 'categorias'
    paginate_by = 50

    def get_queryset(self):
        return get_admin_categories()


class AdminCategoryDeleteView(StaffRequiredMixin, DeleteView):
    model = Category
    template_name = 'admin_panel/category_confirm_delete.html'
    context_object_name = 'categoria'

    def get_success_url(self):
        messages.success(self.request, 'Categoria excluída com sucesso.')
        return self.request.META.get(
            'HTTP_REFERER',
            '/admin-panel/categorias/',
        )
