from django.shortcuts import render


# === PAINEL PRINCIPAL ===
def dashboard(request):
    return render(request, "dashboard.html")


# === MEDICAÇÕES ===
def listar_medicacoes(request):
    return render(request, "medicacoes/listar.html")


def form_medicacao(request):
    return render(request, "medicacoes/form.html")


# === LEMBRETES ===
def listar_lembretes(request):
    return render(request, "lembretes/listar.html")


# === ESTOQUE ===
def listar_estoque(request):
    return render(request, "estoques/listar.html")


# === REGISTROS ===
def listar_registros(request):
    return render(request, "registros/listar.html")
    