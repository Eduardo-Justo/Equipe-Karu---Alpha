from django.urls import path
from . import views

urlpatterns = [
    # === PAINEL PRINCIPAL ===
    path('', views.dashboard, name='dashboard'),

    # === MEDICAÇÕES ===
    # Listar todas
    path('medicacoes/', views.listar_medicacoes, name='listar_medicacoes'),
    # Criar nova (nome ajustado para bater com o template)
    path('medicacoes/nova/', views.criar_medicacao, name='criar_medicacao'),
    # Editar (adicionado o <int:id> para receber o ID do item)
    path('medicacoes/editar/<int:id>/', views.editar_medicacao, name='editar_medicacao'),

    # === LEMBRETES ===
    path('lembretes/', views.listar_lembretes, name='listar_lembretes'),
    # Adicionei a rota de editar pois o template de lembretes tem um botão de editar
    path('lembretes/editar/<int:id>/', views.editar_lembrete, name='editar_lembrete'),

    # === ESTOQUE ===
    path('estoque/', views.listar_estoque, name='listar_estoque'),

    # === REGISTROS ===
    path('registros/', views.listar_registros, name='listar_registros'),
]
