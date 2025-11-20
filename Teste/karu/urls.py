"""
URL configuration for karu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""
URL configuration for karu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from medicacoes import views  # Importa as views do seu app

urlpatterns = [
    # === ADMINISTRAÇÃO ===
    path('admin/', admin.site.urls),

    # === AUTENTICAÇÃO (ESSENCIAL) ===
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # === DASHBOARD ===
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

    # === REGISTROS ===
    path('registros/', views.listar_registros, name='listar_registros'),
]
