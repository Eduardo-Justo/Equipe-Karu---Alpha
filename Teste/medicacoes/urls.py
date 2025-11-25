from django.urls import path
from . import views

"""
Define as rotas (URLs) da aplicação 'medicacoes'.

Cada rota abaixo aponta para uma função correspondente em views.py.
A organização segue blocos lógicos do sistema: Dashboard, Medicações,
Lembretes, Estoque e Registros.
"""

urlpatterns = [
    # === DASHBOARD PRINCIPAL ===
    path('', views.dashboard, name='dashboard'),

    # === MEDICAÇÕES ===
    path('medicacoes/', views.listar_medicacoes, name='listar_medicacoes'),
    path('medicacoes/nova/', views.criar_medicacao, name='criar_medicacao'),  
    path('medicacoes/editar/<int:id>/', views.editar_medicacao, name='editar_medicacao'),

    # === LEMBRETES ===
    path('lembretes/', views.listar_lembretes, name='listar_lembretes'),
    path('lembretes/novo/', views.criar_lembrete, name='criar_lembrete'),
    path('lembretes/editar/<int:id>/', views.editar_lembrete, name='editar_lembrete'),

    # === ESTOQUE ===
    path('estoque/', views.listar_estoque, name='listar_estoque'),
    path('estoque/novo/', views.criar_estoque, name='criar_estoque'),
    path('estoque/editar/<int:id>/', views.editar_estoque, name='editar_estoque'),

    # === REGISTROS DE ADMINISTRAÇÃO ===
    path('registros/', views.listar_registros, name='listar_registros'),
]
