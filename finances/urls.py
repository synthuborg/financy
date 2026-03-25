from django.urls import path

from . import views

app_name = 'finances'

urlpatterns = [
    # Transações
    path('transacoes/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transacoes/nova/', views.TransactionCreateView.as_view(), name='transaction_create'),
    path('transacoes/<int:pk>/editar/', views.TransactionUpdateView.as_view(), name='transaction_update'),
    path('transacoes/<int:pk>/excluir/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
    # Categorias
    path('categorias/', views.CategoryListView.as_view(), name='category_list'),
    path('categorias/nova/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categorias/<int:pk>/editar/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categorias/<int:pk>/excluir/', views.CategoryDeleteView.as_view(), name='category_delete'),
    # Contas (geral — mantido para compatibilidade)
    path('contas/', views.AccountListView.as_view(), name='account_list'),
    path('contas/nova/', views.AccountCreateView.as_view(), name='account_create'),
    path('contas/<int:pk>/editar/', views.AccountUpdateView.as_view(), name='account_update'),
    path('contas/<int:pk>/excluir/', views.AccountDeleteView.as_view(), name='account_delete'),
    # Contas Correntes
    path('conta-corrente/', views.ContaCorrenteListView.as_view(), name='conta_corrente_list'),
    path('conta-corrente/nova/', views.ContaCorrenteCreateView.as_view(), name='conta_corrente_create'),
    path('conta-corrente/<int:pk>/editar/', views.ContaCorrenteUpdateView.as_view(), name='conta_corrente_update'),
    path('conta-corrente/<int:pk>/excluir/', views.ContaCorrenteDeleteView.as_view(), name='conta_corrente_delete'),
    # Cartões de Crédito
    path('cartao/', views.CartaoCreditoListView.as_view(), name='cartao_credito_list'),
    path('cartao/novo/', views.CartaoCreditoCreateView.as_view(), name='cartao_credito_create'),
    path('cartao/<int:pk>/editar/', views.CartaoCreditoUpdateView.as_view(), name='cartao_credito_update'),
    path('cartao/<int:pk>/excluir/', views.CartaoCreditoDeleteView.as_view(), name='cartao_credito_delete'),
    # Metas
    path('metas/', views.GoalListView.as_view(), name='goal_list'),
    path('metas/nova/', views.GoalCreateView.as_view(), name='goal_create'),
    path('metas/<int:pk>/editar/', views.GoalUpdateView.as_view(), name='goal_update'),
    path('metas/<int:pk>/excluir/', views.GoalDeleteView.as_view(), name='goal_delete'),
    path('metas/<int:pk>/progresso/', views.GoalAddProgressView.as_view(), name='goal_add_progress'),
    # Importação de Extratos
    path('importar/', views.ImportStatementView.as_view(), name='import_statement'),
    # Relatórios
    path('relatorios/', views.ReportView.as_view(), name='report'),
]

