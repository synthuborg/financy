"""
Django CBV Templates with Mixins

Padrões reutilizáveis para Class-Based Views seguindo PEP08
"""

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import Http404


# ============================================================================
# Mixins Customizados
# ============================================================================

class UserOwnershipMixin(UserPassesTestMixin):
    """
    Verifica se o usuário é o proprietário do objeto.
    Use em views de detalhe, edição e deleção.
    """
    
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class PaginationMixin:
    """
    Aplica paginação padrão.
    """
    paginate_by = 20
    
    def get_paginate_by(self, queryset):
        return self.request.GET.get('paginate_by', self.paginate_by)


class SearchMixin:
    """
    Adiciona busca ao queryset.
    Subclasses devem definir search_fields.
    """
    search_fields = []
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        
        if query and self.search_fields:
            from django.db.models import Q
            q_objects = Q()
            for field in self.search_fields:
                q_objects |= Q(**{f'{field}__icontains': query})
            queryset = queryset.filter(q_objects)
        
        return queryset


# ============================================================================
# Exemplo: Lista com paginação e busca
# ============================================================================

class MyModelListView(LoginRequiredMixin, PaginationMixin, SearchMixin,
                      ListView):
    """
    Lista todos os MyModel paginados e com busca.
    """
    model = None  # Definir na subclasse
    template_name = 'myapp/mymodel_list.html'
    context_object_name = 'objects'
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


# ============================================================================
# Exemplo: Detalhe com propriedade
# ============================================================================

class MyModelDetailView(LoginRequiredMixin, UserOwnershipMixin, DetailView):
    """
    Mostra detalhe de um MyModel se o usuário é o proprietário.
    """
    model = None  # Definir na subclasse
    template_name = 'myapp/mymodel_detail.html'
    context_object_name = 'object'


# ============================================================================
# Exemplo: Criar com validação de formulário
# ============================================================================

class MyModelCreateView(LoginRequiredMixin, CreateView):
    """
    Cria novo MyModel associado ao usuário logado.
    """
    model = None  # Definir na subclasse
    form_class = None  # Definir na subclasse
    template_name = 'myapp/mymodel_form.html'
    success_url = reverse_lazy('myapp:mymodel-list')
    
    def form_valid(self, form):
        """Associa o objeto ao usuário atual antes de salvar."""
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Criar'
        return context


# ============================================================================
# Exemplo: Atualizar com propriedade
# ============================================================================

class MyModelUpdateView(LoginRequiredMixin, UserOwnershipMixin, UpdateView):
    """
    Atualiza um MyModel se o usuário é o proprietário.
    """
    model = None  # Definir na subclasse
    form_class = None  # Definir na subclasse
    template_name = 'myapp/mymodel_form.html'
    success_url = reverse_lazy('myapp:mymodel-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Editar'
        return context


# ============================================================================
# Exemplo: Deletar com confirmação
# ============================================================================

class MyModelDeleteView(LoginRequiredMixin, UserOwnershipMixin, DeleteView):
    """
    Deleta um MyModel se o usuário é o proprietário.
    """
    model = None  # Definir na subclasse
    template_name = 'myapp/mymodel_confirm_delete.html'
    success_url = reverse_lazy('myapp:mymodel-list')


# ============================================================================
# Exemplo: Implementação Concreta
# ============================================================================

from django.views.generic import FormView


class ExpenseListView(LoginRequiredMixin, PaginationMixin, SearchMixin,
                      ListView):
    """Exemplo concreto: lista de despesas."""
    model = None  # from .models import Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'
    paginate_by = 20
    search_fields = ['description', 'category']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user=self.request.user
        ).order_by('-date')


# ============================================================================
# Notas de Implementação
# ============================================================================

"""
1. HERANÇA MÚLTIPLA
   - Ordem importa: RequerimentosMixin primeiro (LoginRequiredMixin)
   - Depois mixins customizados (PaginationMixin, SearchMixin)
   - View genérica por último (ListView, CreateView)

2. MODEL E FORM
   - Sempre redefinir em subclasses concretas
   - Usar type hints se possível (Python 3.5+)

3. QUERYSET
   - Sempre filtrar por usuário em get_queryset()
   - Usar order_by() para ordenação consistente

4. CONTEXT
   - Usar context_object_name descritivo
   - Adicionar metadados em get_context_data()

5. URLS
   Exemplo de url.py:
   
   from django.urls import path
   from . import views
   
   app_name = 'myapp'
   urlpatterns = [
       path('', views.MyModelListView.as_view(), name='mymodel-list'),
       path('<int:pk>/', views.MyModelDetailView.as_view(), 
            name='mymodel-detail'),
       path('criar/', views.MyModelCreateView.as_view(), 
            name='mymodel-create'),
       path('<int:pk>/editar/', views.MyModelUpdateView.as_view(), 
            name='mymodel-update'),
       path('<int:pk>/deletar/', views.MyModelDeleteView.as_view(), 
            name='mymodel-delete'),
   ]
"""
