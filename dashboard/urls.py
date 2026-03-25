from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path(
        'htmx/grafico-evolucao/',
        views.GraficoEvolucaoView.as_view(),
        name='grafico_evolucao',
    ),
    path(
        'htmx/grafico-saidas/',
        views.GraficoSaidasView.as_view(),
        name='grafico_saidas',
    ),
    path(
        'htmx/grafico-metas/',
        views.GraficoMetasView.as_view(),
        name='grafico_metas',
    ),
    path(
        'htmx/grafico-investimentos/',
        views.GraficoInvestimentosView.as_view(),
        name='grafico_investimentos',
    ),
]
