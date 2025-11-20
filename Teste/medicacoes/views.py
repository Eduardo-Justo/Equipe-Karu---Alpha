from django.shortcuts import render, redirect, get_object_or_404
# Importe seus models aqui quando tiver eles criados, ex:
# from .models import Medicacao, Lembrete, Estoque, Registro
# from .forms import MedicacaoForm

# === PAINEL PRINCIPAL ===
def dashboard(request):
    # Aqui você futuramente fará queries para preencher os cards de resumo
    return render(request, "dashboard.html")


# === MEDICAÇÕES ===
def listar_medicacoes(request):
    # Busque do banco: medicacoes = Medicacao.objects.all()
    medicacoes = [] # Lista vazia por enquanto para não dar erro
    
    context = {
        'medicacoes': medicacoes
    }
    return render(request, "medicacoes/listar.html", context)

def criar_medicacao(request):
    # Lógica do Form aqui (POST vs GET)
    if request.method == 'POST':
        # form = MedicacaoForm(request.POST)
        # if form.is_valid(): form.save(); return redirect('listar_medicacoes')
        pass
    
    # form = MedicacaoForm()
    context = {
        'titulo': 'Nova Medicação',
        'form': [] # Passe o form real aqui
    }
    return render(request, "medicacoes/form.html", context)

def editar_medicacao(request, id):
    # med = get_object_or_404(Medicacao, id=id)
    # Lógica de update...
    
    context = {
        'titulo': f'Editar Medicação #{id}', # Exibe o ID no título
        'form': [] 
    }
    return render(request, "medicacoes/form.html", context)


# === LEMBRETES ===
def listar_lembretes(request):
    # lembretes = Lembrete.objects.all()
    lembretes = []
    return render(request, "lembretes/listar.html", {'lembretes': lembretes})

def editar_lembrete(request, id):
    # Lógica de edição de lembrete
    # return render(request, "lembretes/form.html", ...)
    # Por enquanto redireciona para lista ou renderiza um form placeholder
    return render(request, "lembretes/listar.html", {})


# === ESTOQUE ===
def listar_estoque(request):
    # estoques = Estoque.objects.all()
    estoques = []
    return render(request, "estoques/listar.html", {'estoques': estoques})


# === REGISTROS ===
def listar_registros(request):
    # registros = Registro.objects.all().order_by('-horario_registro')
    registros = []
    return render(request, "registros/listar.html", {'registros': registros})