# medicacoes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("medicacoes/", views.lista_medicacoes, name="lista_medicacoes"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]