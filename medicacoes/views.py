from django.shortcuts import render
from .models import Medicacao

def lista_medicacoes(request):
    medicacoes = Medicacao.objects.all()
    return render(request, "medicacoes/medicacao_lista.html", {"medicacoes": medicacoes})
def admin_dashboard(request):
    return render(request, "medicacoes/admin_dashboard.html")
