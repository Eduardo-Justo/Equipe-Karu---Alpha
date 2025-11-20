from django.urls import path
from . import views

urlpatterns = [
    # Dashboard local (opcional)
    path('', views.dashboard, name='dashboard'),

    # Medicações
    path('listar/', views.listar_medicacoes, name='listar_medicacoes'),
    path('novo/', views.form_medicacao, name='nova_medicacao'),

    # Lembretes
    path('lembretes/', views.listar_lembretes, name='listar_lembretes'),

    # Estoque
    path('estoque/', views.listar_estoque, name='listar_estoque'),

    # Registros
    path('registros/', views.listar_registros, name='listar_registros'),
]
