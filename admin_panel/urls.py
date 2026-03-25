from django.urls import path

from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='dashboard'),
    path('usuarios/', views.AdminUserListView.as_view(), name='user_list'),
    path(
        'usuarios/<int:pk>/toggle/',
        views.AdminUserToggleView.as_view(),
        name='user_toggle',
    ),
    path(
        'transacoes/',
        views.AdminTransactionListView.as_view(),
        name='transaction_list',
    ),
    path(
        'transacoes/<int:pk>/excluir/',
        views.AdminTransactionDeleteView.as_view(),
        name='transaction_delete',
    ),
    path(
        'categorias/',
        views.AdminCategoryListView.as_view(),
        name='category_list',
    ),
    path(
        'categorias/<int:pk>/excluir/',
        views.AdminCategoryDeleteView.as_view(),
        name='category_delete',
    ),
]
