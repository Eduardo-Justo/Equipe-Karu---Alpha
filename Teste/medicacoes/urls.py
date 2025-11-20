from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Medicações
    path('medicacoes/', views.listar_medicacoes, name='listar_medicacoes'),
    path('medicacoes/novo/', views.form_medicacao, name='nova_medicacao'),

    # Lembretes
    path('lembretes/', views.listar_lembretes, name='listar_lembretes'),

    # Estoque
    path('estoque/', views.listar_estoque, name='listar_estoque'),

    # Registros
    path('registros/', views.listar_registros, name='listar_registros'),
]
