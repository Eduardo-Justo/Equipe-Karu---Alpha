"""
URL configuration for the 'karu' project.

Este arquivo define todas as rotas principais do sistema,
incluindo:

- Login híbrido (mock + Django)
- Área dos pais/cuidadores (modo demonstrativo)
- Dashboard real (admin interno)
- CRUD de Medicações, Lembretes, Estoque e Registros

Nada da lógica foi alterado — apenas organização e comentários úteis.
"""

from django.contrib import admin
from django.urls import path
from medicacoes import views  # Importa as views do app

urlpatterns = [
    # ==============================
    # ADMINISTRAÇÃO NATIVA DO DJANGO
    # ==============================
    path('admin/', admin.site.urls),

    # ==============================
    # LOGIN / LOGOUT PERSONALIZADOS
    # ==============================
    # Login híbrido: tenta usuário fake -> depois Django real
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ==============================
    # ÁREA DOS PAIS (MOCKUP)
    # ==============================
    path('area-pais/', views.area_pais, name='area_pais'),
    path('simular-acao/', views.simular_registro_pai, name='simular_registro_pai'),

    # ==============================
    # DASHBOARD (ADMIN REAL)
    # ==============================
    path('', views.dashboard, name='dashboard'),

    # ==============================
    # MEDICAÇÕES — CRUD
    # ==============================
    path('medicacoes/', views.listar_medicacoes, name='listar_medicacoes'),
    path('medicacoes/nova/', views.criar_medicacao, name='criar_medicacao'),
    path('medicacoes/editar/<int:id>/', views.editar_medicacao, name='editar_medicacao'),

    # ==============================
    # LEMBRETES — CRUD
    # ==============================
    path('lembretes/', views.listar_lembretes, name='listar_lembretes'),
    path('lembretes/novo/', views.criar_lembrete, name='criar_lembrete'),
    path('lembretes/editar/<int:id>/', views.editar_lembrete, name='editar_lembrete'),

    # ==============================
    # ESTOQUE — CRUD
    # ==============================
    path('estoque/', views.listar_estoque, name='listar_estoque'),
    path('estoque/novo/', views.criar_estoque, name='criar_estoque'),
    path('estoque/editar/<int:id>/', views.editar_estoque, name='editar_estoque'),

    # ==============================
    # REGISTROS (Histórico de ações)
    # ==============================
    path('registros/', views.listar_registros, name='listar_registros'),
]
